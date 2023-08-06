from .embeddings import PositionalEmbedding, SinusoidalPositionalEmbedding
from .layers import TransformerDecoderLayer, TransformerEncoderLayer
try:
    from apex.normalization.fused_layer_norm import FusedLayerNorm
    LayerNorm = FusedLayerNorm
except ImportError as e:
    from torch.nn.modules import LayerNorm

