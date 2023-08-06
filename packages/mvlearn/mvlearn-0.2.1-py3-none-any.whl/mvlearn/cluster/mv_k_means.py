# Copyright 2019 NeuroData (http://neurodata.io)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Implements multi-view kmeans clustering algorithm for data with 2-views.


import numpy as np
from .base_cluster import BaseCluster
from ..utils.utils import check_Xs
from sklearn.exceptions import NotFittedError, ConvergenceWarning
from scipy.spatial.distance import cdist


class MultiviewKMeans(BaseCluster):

    '''
    An implementation of Multi-View K-Means using the co-EM algorithm.
    This algorithm currently handles two views of data.

    Parameters
    ---------
    n_clusters : int, optional, default=2
        The number of clusters

    random_state : int, optional, default=None
        Determines random number generation for initializing centroids.
        Can seed the random number generator with an int.

    patience : int, optional, default=5
        The number of EM iterations with no decrease in the objective
        function after which the algorithm will terminate.

    max_iter : int, optional, default=None
        The maximum number of EM iterations to run before
        termination.

    n_init : int, optional, default=5
        Number of times the k-means algorithm will run on different
        centroid seeds. The final result will be the best output of
        n_init runs with respect to total inertia across all views.

    Attributes
    ----------

    centroids_ : list of array-likes
        - centroids_ length: n_views
        - centroids_[i] shape: (n_clusters, n_features_i)
        The cluster centroids for each of the two views. centroids_[0]
        corresponds to the centroids of view 1 and centroids_[1] corresponds
        to the centroids of view 2.

    References
    ----------
    [1] Bickel S, Scheffer T (2004) Multi-view clustering. Proceedings of the
    4th IEEE International Conference on Data Mining, pp. 19–26
    '''

    def __init__(self, n_clusters=2, random_state=None,
                 patience=5, max_iter=None, n_init=5):

        super().__init__()

        if not (isinstance(n_clusters, int) and n_clusters > 0):
            msg = 'n_clusters must be a positive integer'
            raise ValueError(msg)

        if random_state is not None:
            msg = 'random_state must be convertible to 32 bit unsigned integer'
            try:
                random_state = int(random_state)
            except ValueError:
                raise ValueError(msg)
            np.random.seed(random_state)

        if not (isinstance(patience, int) and (patience > 0)):
            msg = 'patience must be a nonnegative integer'
            raise ValueError(msg)

        self.max_iter = None
        if max_iter is not None:
            if not (isinstance(max_iter, int) and (max_iter > 0)):
                msg = 'max_iter must be a positive integer'
                raise ValueError(msg)
            self.max_iter = max_iter

        if not (isinstance(n_init, int) and (n_init > 0)):
            msg = 'n_init must be a nonnegative integer'
            raise ValueError(msg)

        self.n_clusters = n_clusters
        self.random_state = random_state
        self.patience = patience
        self.n_init = n_init
        self.centroids_ = None

    def _final_centroids(self, Xs, centroids):

        '''
        Compute the final cluster centroids based on consensus samples across
        both views. Consensus samples are those that are assigned to the same
        partition in both views.

        Parameters
        ----------
        Xs : list of array-likes or numpy.ndarray
            - Xs length: n_views
            - Xs[i] shape: (n_samples, n_features_i)
            This list must be of size 2, corresponding to the two views of
            the data. The two views can each have a different number of
            features, but they must have the same number of samples.


        centroids_ : list of array-likes
            - centroids length: n_views
            - centroids[i] shape: (n_clusters, n_features_i)
            The cluster centroids for each of the two views. centroids[0]
            corresponds to the centroids of view 1 and centroids[1] corresponds
            to the centroids of view 2. These are not yet the final cluster
            centroids.
        '''

        # Compute consensus vectors for final clustering
        v1_consensus = list()
        v2_consensus = list()

        for clust in range(self.n_clusters):
            v1_distances = cdist(Xs[0], centroids[0])
            v1_partitions = np.argmin(v1_distances, axis=1).flatten()
            v2_distances = cdist(Xs[1], centroids[1])
            v2_partitions = np.argmin(v2_distances, axis=1).flatten()

            # Find data points in the same partition in both views
            part_indices = (v1_partitions == clust) * (v2_partitions == clust)

            # Recompute centroids based on these data points
            if (np.sum(part_indices) != 0):
                cent1 = np.mean(Xs[0][part_indices], axis=0)
                v1_consensus.append(cent1)

                cent2 = np.mean(Xs[1][part_indices], axis=0)
                v2_consensus.append(cent2)

        # Check if there are no consensus vectors
        self.centroids_ = [None, None]
        if (len(v1_consensus) == 0):
            msg = 'No distinct cluster centroids have been found.'
            raise ConvergenceWarning(msg)
        else:
            self.centroids_[0] = np.vstack(v1_consensus)
            self.centroids_[1] = np.vstack(v2_consensus)

            # Check if the number of consensus clusters is less than n_clusters
            if (self.centroids_[0].shape[0] < self.n_clusters):
                msg = ('Number of distinct cluster centroids ('
                       + str(self.centroids_[0].shape[0])
                       + ') found is smaller than n_clusters ('
                       + str(self.n_clusters)
                       + ').')
                raise ConvergenceWarning(msg)

            # Updates k if number of consensus clusters less than original
            # n_clusters value
            self.n_clusters = self.centroids_[0].shape[0]

    def fit(self, Xs):

        '''
        Fit the cluster centroids to the data.

        Parameters
        ----------
        Xs : list of array-likes or numpy.ndarray
            - Xs length: n_views
            - Xs[i] shape: (n_samples, n_features_i)
            This list must be of size 2, corresponding to the two views of
            the data. The two views can each have a different number of
            features, but they must have the same number of samples.

        Returns
        -------
        self : returns an instance of self.
        '''

        Xs = check_Xs(Xs, enforce_views=2)

        # Run multi-view kmeans for n_init different centroid initializations
        min_inertia = np.inf
        best_centroids = None

        for _ in range(self.n_init):

            # Random initialization of centroids
            indices1 = np.random.choice(Xs[0].shape[0], self.n_clusters)
            centers1 = Xs[0][indices1]
            indices2 = np.random.choice(Xs[1].shape[0], self.n_clusters)
            centers2 = Xs[1][indices2]
            centroids = [centers1, centers2]

            # Initializing partitions, objective value, and loop vars
            distances = cdist(Xs[1], centers2)
            parts = np.argmin(distances, axis=1).flatten()
            partitions = [None, parts]
            objective = [np.inf, np.inf]
            iter_stall = 0
            iter_num = 0

            # While objective is still decreasing and iterations < max_iter
            max_iter = np.inf
            if self.max_iter is not None:
                max_iter = self.max_iter
            while(iter_stall < self.patience and iter_num < max_iter):
                iter_num += 1
                pre_view = (iter_num) % 2
                view = (iter_num + 1) % 2
                # Switch partitions and compute maximization
                new_centers = list()
                for cl in range(self.n_clusters):
                    # Recompute centroids using samples from each cluster
                    mask = (partitions[pre_view] == cl)
                    if (np.sum(mask) == 0):
                        new_centers.append(centroids[view][cl])
                    else:
                        cent = np.mean(Xs[view][mask], axis=0)
                        new_centers.append(cent)
                centroids[view] = np.vstack(new_centers)

                # Compute expectation
                distances = cdist(Xs[view], centroids[view])
                partitions[view] = np.argmin(distances, axis=1).flatten()
                # Recompute the objective function
                o_funct = 0
                for cl in range(self.n_clusters):
                    # Collect data points in each cluster and compute within
                    # cluster distances
                    vecs = Xs[view][(partitions[view] == cl)]
                    dist = np.linalg.norm(vecs - centroids[view][cl], axis=1)
                    o_funct += np.sum(dist)

                # Track of number of iterations without improvement
                if(o_funct < objective[view]):
                    objective[view] = o_funct
                    iter_stall = 0
                else:
                    iter_stall += 1

            # Update min_intertia and best centroids if lower intertia
            total_inertia = np.sum(objective)
            if(total_inertia < min_inertia or best_centroids is None):
                min_inertia = total_inertia
                best_centroids = centroids

        # Compute final cluster centroids
        self._final_centroids(Xs, best_centroids)

        return self

    def predict(self, Xs):

        '''
        Predict the cluster labels for the data.

        Parameters
        ----------
        Xs : list of array-likes or numpy.ndarray
            - Xs length: n_views
            - Xs[i] shape: (n_samples, n_features_i)
            This list must be of size 2, corresponding to the two
            views of the data. The two views can each have a different
            number of features, but they must have the same number of samples.

        Returns
        -------
        predictions : array-like, shape (n_samples,)
            The predicted cluster labels for each sample.

        '''

        Xs = check_Xs(Xs, enforce_views=2)

        if self.centroids_ is None:
            msg = 'This MultiviewKMeans instance is not fitted yet.'
            raise NotFittedError(msg)

        if self.centroids_[0] is None:
            msg = 'This MultiviewKMeans instance has no cluster centroids.'
            raise AttributeError(msg)

        dist1 = cdist(Xs[0], self.centroids_[0])
        dist2 = cdist(Xs[1], self.centroids_[1])
        dist_metric = dist1 + dist2
        predictions = np.argmin(dist_metric, axis=1).flatten()

        return predictions
