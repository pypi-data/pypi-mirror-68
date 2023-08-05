import torch.nn.functional as F

# from apex.normalization.fused_layer_norm import FusedLayerNorm
from torch import nn
from torch.nn.modules import Linear
from torch.nn.modules.activation import MultiheadAttention


# copied from mlperf
def dropout_add(x, residual, prob, is_training):
    out = F.dropout(x, p=prob, training=is_training)
    out = residual + out
    return out


# copied from mlperf
def relu_dropout(x, prob, is_training):
    out = F.threshold(x, 0.0, 0.0)
    out = F.dropout(out, p=prob, training=is_training)
    return out


# copied from mlperf
class TransformerEncoderLayer(nn.Module):
    """Encoder layer block.

    In the original paper each operation (multi-head attention or FFN) is
    postprocessed with: `dropout -> add residual -> layernorm`. In the
    tensor2tensor code they suggest that learning is more robust when
    preprocessing each layer with layernorm and postprocessing with:
    `dropout -> add residual`. We default to the approach in the paper, but the
    tensor2tensor approach can be enabled by setting
    *args.encoder_normalize_before* to ``True``.

    Args:
        args (argparse.Namespace): parsed command-line arguments
    """

    def __init__(self, args):
        super().__init__()
        self.embed_dim = args.encoder_embed_dim
        self.self_attn = MultiheadAttention(
            embed_dim=self.embed_dim,
            num_heads=args.encoder_attention_heads,
            dropout=args.attention_dropout,
        )
        self.dropout = args.dropout
        self.relu_dropout = args.relu_dropout
        self.fuse_dropout_add = args.fuse_dropout_add
        self.fuse_relu_dropout = args.fuse_relu_dropout
        self.normalize_before = args.encoder_normalize_before
        self.fc1 = Linear(self.embed_dim, args.encoder_ffn_embed_dim)
        self.fc2 = Linear(args.encoder_ffn_embed_dim, self.embed_dim)
        self.layer_norms = nn.ModuleList(
            [nn.LayerNorm(self.embed_dim) for _ in range(2)]
        )

    def forward(self, x, encoder_padding_mask):
        residual = x

        x = self.maybe_layer_norm(0, x, before=True)
        x, _ = self.self_attn(
            query=x, key=x, value=x, key_padding_mask=encoder_padding_mask
        )

        if self.fuse_dropout_add and self.training:
            raise ValueError("Cannot use fused_dropout_add yet")
            # x = fused_dropout_add(x, residual, self.dropout)
        else:
            x = dropout_add(x, residual, self.dropout, self.training)

        x = self.maybe_layer_norm(0, x, after=True)

        residual = x
        x = self.maybe_layer_norm(1, x, before=True)

        # Fuse Bias to GEMMs by making Tensors 2D
        sent_len, sents, hid_dim = x.size()
        x = x.view(sent_len * sents, hid_dim)
        if self.fuse_relu_dropout:
            # x = fused_relu_dropout(self.fc1(x), self.relu_dropout)
            raise ValueError("Cannot use fused_dropout_add yet")
        else:
            x = relu_dropout(self.fc1(x), self.relu_dropout, self.training)

        x = self.fc2(x)
        x = x.view(sent_len, sents, hid_dim)

        if self.fuse_dropout_add and self.training:
            # x = fused_dropout_add(x, residual, self.dropout)
            raise ValueError("Cannot use fused_dropout_add yet")
        else:
            x = dropout_add(x, residual, self.dropout, self.training)
        x = self.maybe_layer_norm(1, x, after=True)
        return x

    def maybe_layer_norm(self, i, x, before=False, after=False):
        assert before ^ after
        if after ^ self.normalize_before:
            return self.layer_norms[i](x)
        else:
            return x


# copied from mlperf
class TransformerDecoderLayer(nn.Module):
    """Decoder layer block.

    In the original paper each operation (multi-head attention, encoder
    attention or FFN) is postprocessed with: `dropout -> add residual ->
    layernorm`. In the tensor2tensor code they suggest that learning is more
    robust when preprocessing each layer with layernorm and postprocessing with:
    `dropout -> add residual`. We default to the approach in the paper, but the
    tensor2tensor approach can be enabled by setting
    *args.decoder_normalize_before* to ``True``.

    Args:
        args (argparse.Namespace): parsed command-line arguments
        no_encoder_attn (bool, optional): whether to attend to encoder outputs
            (default: False).
    """

    def __init__(self, args, no_encoder_attn=False):
        super().__init__()
        self.embed_dim = args.decoder_embed_dim
        self.self_attn = MultiheadAttention(
            embed_dim=self.embed_dim,
            num_heads=args.decoder_attention_heads,
            dropout=args.attention_dropout,
        )
        self.dropout = args.dropout
        self.relu_dropout = args.relu_dropout
        self.normalize_before = args.decoder_normalize_before
        self.fuse_dropout_add = args.fuse_dropout_add
        self.fuse_relu_dropout = args.fuse_relu_dropout

        self.self_attn_layer_norm = nn.LayerNorm(self.embed_dim)

        if no_encoder_attn:
            self.encoder_attn = None
            self.encoder_attn_layer_norm = None
        else:
            self.encoder_attn = MultiheadAttention(
                embed_dim=self.embed_dim,
                num_heads=args.decoder_attention_heads,
                dropout=args.attention_dropout,
            )
            self.encoder_attn_layer_norm = nn.LayerNorm(self.embed_dim)

        self.fc1 = Linear(self.embed_dim, args.decoder_ffn_embed_dim)
        self.fc2 = Linear(args.decoder_ffn_embed_dim, self.embed_dim)

        self.final_layer_norm = nn.LayerNorm(self.embed_dim)
        self.need_attn = True

    def forward(self, x, encoder_out, encoder_padding_mask, incremental_state=None):
        residual = x
        x = self.maybe_layer_norm(self.self_attn_layer_norm, x, before=True)
        x, _ = self.self_attn(
            query=x,
            key=x,
            value=x,
            # mask_future_timesteps=True,
            # incremental_state=incremental_state,
            need_weights=False,
        )
        if self.fuse_dropout_add and self.training:
            # x = fused_dropout_add(x, residual, self.dropout)
            raise ValueError("Cannot use fused_dropout_add yet")
        else:
            x = dropout_add(x, residual, self.dropout, self.training)
        x = self.maybe_layer_norm(self.self_attn_layer_norm, x, after=True)

        attn = None
        if self.encoder_attn is not None:
            residual = x
            x = self.maybe_layer_norm(self.encoder_attn_layer_norm, x, before=True)
            x, attn = self.encoder_attn(
                query=x,
                key=encoder_out,
                value=encoder_out,
                key_padding_mask=encoder_padding_mask,
                # incremental_state=incremental_state,
                # static_kv=True,
                need_weights=(not self.training and self.need_attn),
            )
            if self.fuse_dropout_add and self.training:
                raise ValueError("Cannot use fused_dropout_add yet")
            else:
                x = dropout_add(x, residual, self.dropout, self.training)

            x = self.maybe_layer_norm(self.encoder_attn_layer_norm, x, after=True)

        residual = x
        x = self.maybe_layer_norm(self.final_layer_norm, x, before=True)

        # Fuse Bias to GEMMs by making Tensors 2D
        sent_len, sents, hid_dim = x.size()
        x = x.view(sent_len * sents, hid_dim)
        if self.fuse_relu_dropout:
            # x = fused_relu_dropout(self.fc1(x), self.relu_dropout)
            raise ValueError("Cannot use fused_dropout_add yet")
        else:
            x = relu_dropout(self.fc1(x), self.relu_dropout, self.training)

        x = self.fc2(x)
        x = x.view(sent_len, sents, hid_dim)

        if self.fuse_dropout_add and self.training:
            raise ValueError("Cannot use fused_dropout_add yet")
            # x = fused_dropout_add(x, residual, self.dropout)
        else:
            x = dropout_add(x, residual, self.dropout, self.training)
        x = self.maybe_layer_norm(self.final_layer_norm, x, after=True)
        return x, attn

    def maybe_layer_norm(self, layer_norm, x, before=False, after=False):
        assert before ^ after
        if after ^ self.normalize_before:
            return layer_norm(x)
        else:
            return x

    def make_generation_fast_(self, need_attn=False, **kwargs):
        self.need_attn = need_attn
