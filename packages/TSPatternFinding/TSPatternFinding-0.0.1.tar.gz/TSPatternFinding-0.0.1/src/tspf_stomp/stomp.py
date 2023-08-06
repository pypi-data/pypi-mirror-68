import argparse
from matrixprofile import *
import numpy as np

class TSPFStomp:
    def __init__(self, infile="", indir="", outdir=""): 
        pass
    
    def locate(self, timeseries, shapes, threshold=1):
        """
        Given a timeseries, a pattern and optional thresholding,
        return all times where pattern is found in timeseries.
        -------------------------
        Input:
        timeseries - array of y-values (assumed values at consistent time steps)
        motifs - list of time series, each a motif w/ same time grainularity as given timeseries
        threshold  - thresholding for MatrixProfile
        
        Returns:
        List of tuples: (Motif duration in time steps, MatrixProfile value, [list of start of motif] )
        """
        last_index = len(timeseries)
        _motif_indexes = []
        
        if len(shapes) == 0:
            return []
        
        _ts = timeseries
        # Add motifs to the timeseries at the end
        # track where each motif is added in.
        max_len = 0
        min_len = len(shapes[0])
        for s in shapes:
            _motif_indexes.append(last_index)
            _ts = np.append(_ts, s)
            last_index = len(_ts)
            if len(s) > max_len:
                max_len = len(s) + 4
            if len(s) < min_len:
                min_len = max(4, int(len(s)/2))
        
        _discovered = self.discover(_ts, threshold=int(threshold), min_duration=int(min_len), max_duration=int(max_len))
        
        found = []
        
        for tup in _discovered:
            duration, mp_val, indexes = tup
            found_motif = False
            found_motif_index = -1
            indexes_to_keep = []
            for i in indexes:
                if i < len(timeseries):
                    found_motif = True
                    indexes_to_keep.append(i)
                else:
                    # Appended motif - which one?
                    found_motif_index = self._closest_val(i, _motif_indexes)
            if found_motif and found_motif_index > -1:
                # We successfully found a motif in our search list.
                found.append((tup[0], tup[1], indexes_to_keep))
        
        return found
                
                
    def _closest_val(self, val, lst):
        return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-val))]
        
    
    def motif_shapes_from_tuple(self, tuples, timeseries):
        """
        Given a list of tuples describing time motifs discovered
        in the given timeseries, returns a list of time series,
        one per motif.
        -------------------------
        Input:
        tuples - List of tuples: (Motif duration in time steps, MatrixProfile value, [list of start of motif])
        timeseries - array of y-values motifs were discovered in
        
        Returns:
        List of arrays of y-values describing motif shapes.
        """
        
        shapes = []
        
        for tup in tuples:
            duration, mp_val, indexes = tup
            try:
                shape = timeseries[indexes[0]:indexes[0]+duration-1]            
                shapes.append(shape)
            except IndexError:
                print("Given motif tuple does not describe motif in given timeseries.", file=sys.stderr)
                pass
        
        return shapes
        
    def discover(self, timeseries, threshold=1, min_duration=10, max_duration=600):
        """
        Given a timeseries, identify common motifs.
        Return list of motifs, and where in timeseries 
        they're found.
        -------------------------
        Input:
        timeseries - array of y-values (assumed values at consistent time steps)
        threshold  - thresholding for MatrixProfile
        min_duration - min length of motif to look for in number of time steps 
        max_duration - max length of motif to look for in number of time steps
        
        Returns:
        List of tuples: (Motif duration in time steps, MatrixProfile value, [list of start of motif] )
        """        
        motif_list = []
        # Run a range of MatrixProfiles with different lengths
        m = min_duration
        while m < min(int(len(timeseries)/10), max_duration):
            mp = matrixProfile.stomp(timeseries, m)
            motif_indexes, distances = self._discover(timeseries, mp)
            
            tmp_motif_list = list(zip(distances, motif_indexes))
            
            # Save only motifs which are within the threshold.
            motif_list = motif_list + [ (m, tup[0], tup[1]) for tup in tmp_motif_list if tup[0] < threshold]
            
            # Larger steps as we're looking at larger m values.
            m = m + int(max(1, .05*m))
    
        motif_list = sorted(motif_list, key=lambda x:(x[1], -len(x[2]), -x[0]))
        
        return motif_list
    
    def timeseries_from_files(self, file_list):
        pass
    
    def filter_candidates(self, motif_list):
        filtered = []
        for tup in motif_list:
            if filtered == []:
                filtered.append(tup)
            else:
                duration, mp_val, indexes = tup
                not_found_list = []
                for i in indexes:	
                    found = False
                    for tup in filtered:
                        for i2 in tup[2]:
                            if i in range(max(0, i2-int(duration/2)), i2+int(duration/2)):
                                found = True
                                continue
                        if found:
                            continue
                    if found:
                        continue
                    else:
                        not_found_list.append(i)
                if len(not_found_list) > 0:
                    newtup = (duration, mp_val, not_found_list)
                    filtered.append(newtup)
        return filtered
    
    def _discover(self,timeseries, mp, max_motifs=3, radius=2, n_neighbors=None, ex_zone=None):
        """
        Modifies motifs() from MatrixProfile
        Discovers top k motifs from a matrix profile 
        Parameters
        ----------
        ts: time series to used to calculate mp
        mp: tuple, (matrix profile numpy array, matrix profile indices)
        max_motifs: the maximum number of motifs to discover
        ex_zone: the number of samples to exclude and set to Inf on either side of a found motifs
            defaults to m/2
        Returns tuple (motifs, distances)
        motifs: a list of lists of indexes representing the motif starting locations.
        distances: list of minimum distances for each motif
        """

        motifs = []
        distances = []
        try:
            mp_current, mp_idx = mp
        except TypeError:
            raise ValueError("argument mp must be a tuple")
        mp_current = np.copy(mp_current)

        if len(timeseries) <= 1 or len(mp_current) <= 1 or max_motifs == 0:
            return [], []

        m = len(timeseries) - len(mp_current) + 1
        if m <= 1:
            raise ValueError('Matrix profile is longer than time series.')
        if ex_zone is None:
            ex_zone = m / 2

        for j in range(max_motifs):
            # find minimum distance and index location
            min_idx = mp_current.argmin()
            motif_distance = mp_current[min_idx]
            if motif_distance == np.inf:
                return motifs, distances
            if motif_distance == 0.0:
                motif_distance += np.finfo(mp_current.dtype).eps

            motif_set = set()
            initial_motif = [min_idx]
            pair_idx = int(mp[1][min_idx])
            if mp_current[pair_idx] != np.inf:
                initial_motif += [pair_idx]

            motif_set = set(initial_motif)

            prof, _ = distanceProfile.massDistanceProfile(timeseries, initial_motif[0], m)

            # kill off any indices around the initial motif pair since they are
            # trivial solutions
            for idx in initial_motif:
                self._exclude(prof, idx, ex_zone)
            # exclude previous motifs
            for ms in motifs:
                for idx in ms:
                    self._exclude(prof, idx, ex_zone)

            # keep looking for the closest index to the current motif. Each
            # index found will have an exclusion zone applied as to remove
            # trivial solutions. This eventually exits when there's nothing
            # found within the radius distance.
            prof_idx_sort = prof.argsort()

            for nn_idx in prof_idx_sort:
                if n_neighbors is not None and len(motif_set) >= n_neighbors:
                    break
                if prof[nn_idx] == np.inf:
                    continue
                if prof[nn_idx] < motif_distance * radius:
                    motif_set.add(nn_idx)
                    self._exclude(prof, nn_idx, ex_zone)
                else:
                    break

            for motif in motif_set:
                self._exclude(mp_current, motif, ex_zone)

            if len(motif_set) < 2:
                continue
            motifs += [list(sorted(motif_set))]
            distances += [motif_distance]

        return motifs, distances


    def _exclude(self, prof, idx, zone):
        start = int(max(0, idx - zone))
        end = int(idx + zone + 1)
        prof[start:end] = np.inf        
        
