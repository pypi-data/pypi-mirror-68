# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
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
# ==============================================================================

"""## Generation of summaries.
### Class for writing Summaries
@@FileWriter
@@FileWriterCache
### Summary Ops
@@tensor_summary
@@scalar
@@histogram
@@audio
@@image
@@merge
@@merge_all
## Utilities
@@get_summary_description
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import re as _re
import bisect
from six import StringIO
from six.moves import range
from PIL import Image
import numpy as np
import chainer.cuda
try:
    import cupy
except ImportError:
    print('Not found cupy.')
# pylint: disable=unused-import
from .src.summary_pb2 import Summary
from .src.summary_pb2 import HistogramProto
from .src.summary_pb2 import SummaryMetadata
from .src.tensor_pb2 import TensorProto
from .src.tensor_shape_pb2 import TensorShapeProto

_INVALID_TAG_CHARACTERS = _re.compile(r'[^-/\w\.]')


def _clean_tag(name):
  # In the past, the first argument to summary ops was a tag, which allowed
  # arbitrary characters. Now we are changing the first argument to be the node
  # name. This has a number of advantages (users of summary ops now can
  # take advantage of the tf name scope system) but risks breaking existing
  # usage, because a much smaller set of characters are allowed in node names.
  # This function replaces all illegal characters with _s, and logs a warning.
  # It also strips leading slashes from the name.
  if name is not None:
    new_name = _INVALID_TAG_CHARACTERS.sub('_', name)
    new_name = new_name.lstrip('/')  # Remove leading slashes
    if new_name != name:
      logging.info(
          'Summary name %s is illegal; using %s instead.' %
          (name, new_name))
      name = new_name
  return name


def scalar(name, scalar, collections=None):
    """Outputs a `Summary` protocol buffer containing a single scalar value.
    The generated Summary has a Tensor.proto containing the input Tensor.
    Args:
      name: A name for the generated node. Will also serve as the series name in
        TensorBoard.
      tensor: A real numeric Tensor containing a single value.
      collections: Optional list of graph collections keys. The new summary op is
        added to these collections. Defaults to `[GraphKeys.SUMMARIES]`.
    Returns:
      A scalar `Tensor` of type `string`. Which contains a `Summary` protobuf.
    Raises:
      ValueError: If tensor has the wrong shape or type.
    """
    name = _clean_tag(name)
    if not isinstance(scalar, float):
        # try conversion, if failed then need handle by user.
        scalar = float(scalar)
    return Summary(value=[Summary.Value(tag=name, simple_value=scalar)])


def histogram(name, values, bins, collections=None):
    # pylint: disable=line-too-long
    """Outputs a `Summary` protocol buffer with a histogram.
    The generated
    [`Summary`](https://www.tensorflow.org/code/tensorflow/core/framework/summary.proto)
    has one summary value containing a histogram for `values`.
    This op reports an `InvalidArgument` error if any value is not finite.
    Args:
      name: A name for the generated node. Will also serve as a series name in
        TensorBoard.
      values: A real numeric `Tensor`. Any shape. Values to use to
        build the histogram.
      collections: Optional list of graph collections keys. The new summary op is
        added to these collections. Defaults to `[GraphKeys.SUMMARIES]`.
    Returns:
      A scalar `Tensor` of type `string`. The serialized `Summary` protocol
      buffer.
    """
    name = _clean_tag(name)
    hist = make_histogram(values.astype(float), bins)
    return Summary(value=[Summary.Value(tag=name, histo=hist)])



def make_histogram(values, bins):
    """Convert values into a histogram proto using logic from histogram.cc."""
    values = values.reshape(-1)
    counts, limits = np.histogram(values, bins=bins)
    limits = limits[1:]

    sum_sq = values.dot(values)
    return HistogramProto(min=values.min(),
                          max=values.max(),
                          num=len(values),
                          sum=values.sum(),
                          sum_squares=sum_sq,
                          bucket_limit=limits,
                          bucket=counts)


def image(tag, tensor):
    """Outputs a `Summary` protocol buffer with images.
    The summary has up to `max_images` summary values containing images. The
    images are built from `tensor` which must be 3-D with shape `[height, width,
    channels]` and where `channels` can be:
    *  1: `tensor` is interpreted as Grayscale.
    *  3: `tensor` is interpreted as RGB.
    *  4: `tensor` is interpreted as RGBA.
    The `name` in the outputted Summary.Value protobufs is generated based on the
    name, with a suffix depending on the max_outputs setting:
    *  If `max_outputs` is 1, the summary value tag is '*name*/image'.
    *  If `max_outputs` is greater than 1, the summary value tags are
       generated sequentially as '*name*/image/0', '*name*/image/1', etc.
    Args:
      tag: A name for the generated node. Will also serve as a series name in
        TensorBoard.
      tensor: A 3-D `uint8` or `float32` `Tensor` of shape `[height, width,
        channels]` where `channels` is 1, 3, or 4.
    Returns:
      A scalar `Tensor` of type `string`. The serialized `Summary` protocol
      buffer.
    """
    tag = _clean_tag(tag)
    assert isinstance(tensor, np.ndarray) or isinstance(tensor, cupy.ndarray), 'input tensor should be one of numpy.ndarray, cupy.ndarray'
    if not isinstance(tensor, np.ndarray):
        assert tensor.ndim<4 and tensor.ndim>1, 'input tensor should be 3 dimensional.'
        if tensor.ndim==2:
            tensor = cupy.expand_dims(tensor, 0)
        tensor = chainer.cuda.to_cpu(cupy.transpose(tensor, (1,2,0)))
    else:
        if tensor.ndim==2:
            tensor = np.expand_dims(tensor, 0)
        tensor = np.transpose(tensor, (1,2,0))
        tensor = tensor.astype(np.float32)
    tensor = (tensor*255).astype(np.uint8)
    image = make_image(tensor)
    return Summary(value=[Summary.Value(tag=tag, image=image)])


def make_image(tensor):
    """Convert an numpy representation image to Image protobuf"""
    height, width, channel = tensor.shape
    image = Image.fromarray(tensor)
    import io
    output = io.BytesIO()
    image.save(output, format='PNG')
    image_string = output.getvalue()
    output.close()
    return Summary.Image(height=height,
                         width=width,
                         colorspace=channel,
                         encoded_image_string=image_string)

def video(tag, tensor, fps):
    tag = _clean_tag(tag)
    assert isinstance(tensor, np.ndarray) or isinstance(tensor, cupy.ndarray), 'input tensor should be one of numpy.ndarray, cupy.ndarray'
    if isinstance(tensor, np.ndarray):
        xp = np
    else:
        xp = cupy

    assert tensor.ndim==5, 'input tensor should be 5 dimensional. (batch, channels, time, height, width)'
        
    b, c, t, h, w = tensor.shape

    if tensor.dtype == xp.uint8:
        tensor = xp.float32(tensor) / 255.

    def is_power2(num):
        return num != 0 and ((num & (num - 1)) == 0)

    # pad to power of 2
    while not is_power2(tensor.shape[0]):
        tensor = xp.concatenate((tensor, xp.zeros(shape=(1, c, t, h, w))), axis=0)

    b = tensor.shape[0]
    n_rows = 2**(int(xp.log(b) / xp.log(2)) // 2)
    n_cols = b // n_rows

    tensor = np.reshape(tensor, newshape=(n_rows, n_cols, c, t, h, w))
    tensor = np.transpose(tensor, axes=(3, 0, 4, 1, 5, 2))
    tensor = np.reshape(tensor, newshape=(t, n_rows * h, n_cols * w, c))
    tensor = tensor.astype(xp.float32)
    tensor = (tensor * 255).astype(xp.uint8)

    tensor = chainer.cuda.to_cpu(tensor)
    video = make_video(tensor, fps)

    return Summary(value=[Summary.Value(tag=tag, image=video)])

def make_video(tensor, fps): 
    try:
        import moviepy.editor as mpy
    except ImportError:
        print('add_video needs package moviepy')
        return
    import tempfile

    t, h, w, c = tensor.shape

    # encode sequence of images into gif string
    clip = mpy.ImageSequenceClip(list(tensor), fps=fps)
    with tempfile.NamedTemporaryFile() as f:
        filename = f.name + '.gif'

    clip.write_gif(filename, verbose=True)
    with open(filename, 'rb') as f:
        tensor_string = f.read()
        return Summary.Image(height=h, width=w, colorspace=c, encoded_image_string=tensor_string)

def audio(tag, tensor, sample_rate=44100):
  tensor = tensor.squeeze()
  assert tensor.ndim==1, 'input tensor should be 1 dimensional.'
  tensor_list = [int(32767.0*x) for x in tensor]
  import io
  import wave
  import struct
  fio = io.BytesIO()
  Wave_write = wave.open(fio, 'wb')
  Wave_write.setnchannels(1)
  Wave_write.setsampwidth(2)
  Wave_write.setframerate(sample_rate)
  tensor_enc = b''
  for v in tensor_list:
    tensor_enc += struct.pack('<h', v)
  
  Wave_write.writeframes(tensor_enc)
  Wave_write.close()
  audio_string = fio.getvalue()
  fio.close()
  audio = Summary.Audio(sample_rate=sample_rate, num_channels=1, length_frames=len(tensor_list), encoded_audio_string=audio_string, content_type='audio/wav')

  return Summary(value=[Summary.Value(tag=tag, audio=audio)])

def text(tag, text):
  import json
  PluginData = [SummaryMetadata.PluginData(plugin_name='text')]
  smd = SummaryMetadata(plugin_data=PluginData)
  tensor = TensorProto(dtype='DT_STRING', string_val=[text.encode(encoding='utf_8')])
  return Summary(value=[Summary.Value(node_name=tag, metadata=smd, tensor=tensor)])
