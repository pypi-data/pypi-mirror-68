# Copyright 2016 Jeff Vierstra

import numpy as np

from .. import load_data
from .track import track

class heatmap_data_track(track):

	def __init__(self, interval, data, **kwargs):
		super(heatmap_data_track, self).__init__(interval, **kwargs)

		self.data = data if data.ndim>1 else data[np.newaxis,:]

	def load_data(self, filepath, column=5, dtype=float):
		self.data = load_data(filepath, interval, [column], dtype).T

	def format_axis(self, ax):
		super(heatmap_data_track, self).format_axis(ax)

		ax.yaxis.set(visible = True, ticks = np.arange(self.data.shape[0]), ticklabels = [])
		#ax.set_ylim([0, self.data.shape[0]])

	def render(self, ax):
		
		self.format_axis(ax)

		x = range(interval.start, interval.end+1)
		y = range(data.shape[0]+1)
		ax.pcolormesh(x, y, self.data, cmap = 'RdPu', vmax=15, rasterized=True)

		super(heatmap_data_track, self).render(ax)