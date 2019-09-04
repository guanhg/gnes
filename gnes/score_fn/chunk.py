from .base import get_unary_score, ScoreCombinedFn


class WeightedChunkScoreFn(ScoreCombinedFn):
    """score = d_chunk.weight * relevance * q_chunk.weight"""

    def __call__(self, last_score: 'gnes_pb2.Response.QueryResponse.ScoredResult.Score',
                 q_chunk: 'gnes_pb2.Chunk',
                 d_chunk: 'gnes_pb2.Chunk', *args, **kwargs):
        q_chunk_weight = get_unary_score(value=q_chunk.weight,
                                         name='query chunk weight',
                                         offset=q_chunk.offset)
        d_chunk_weight = get_unary_score(value=d_chunk.weight,
                                         name='document chunk weight',
                                         doc_id=d_chunk.doc_id,
                                         offset=d_chunk.offset)

        return super().__call__(last_score, q_chunk_weight, d_chunk_weight)

# TODO: write this as a class
#     @staticmethod
#     def eq2(q_chunk: 'gnes_pb2.Chunk', d_chunk: 'gnes_pb2.Chunk',
#             relevance, relevance_cls):
#         """
#         score = d_chunk.weight * relevance * offset_divergence * q_chunk.weight
#         offset_divergence is calculated based on doc_type:
#             TEXT && VIDEO && AUDIO: offset is 1-D
#             IMAGE: offset is 2-D
#         """
#
#         def _cal_divergence(q_chunk: 'gnes_pb2.Chunk', d_chunk: 'gnes_pb2.Chunk'):
#             if q_chunk.offset_nd and d_chunk.offset_nd:
#                 return 1 / (1 + np.sqrt((q_chunk.offset_nd[0] - d_chunk.offset_nd[0]) ** 2 +
#                                         (q_chunk.offset_nd[1] - d_chunk.offset_nd[1]) ** 2))
#             else:
#                 return np.abs(q_chunk.offset - d_chunk.offset)
#
#         score = gnes_pb2.Response.QueryResponse.ScoredResult.Score()
#
#         divergence = _cal_divergence(q_chunk, d_chunk)
#         score.value = d_chunk.weight * relevance * divergence * q_chunk.weight
#         score.explained = json.dumps({
#             'name': 'chunk_scorer_eq2',
#             'operand': [{'name': 'd_chunk_weight',
#                          'value': float(d_chunk.weight),
#                          'doc_id': d_chunk.doc_id,
#                          'offset': d_chunk.offset},
#                         {'name': 'q_chunk_weight',
#                          'value': float(q_chunk.weight),
#                          'offset': q_chunk.offset},
#                         {'name': 'relevance',
#                          'op': relevance_cls,
#                          'operand': [{'name': 'doc_chunk',
#                                       'doc_id': d_chunk.doc_id,
#                                       'offset': d_chunk.offset},
#                                      {'name': 'query_chunk',
#                                       'offset': q_chunk.offset}
#                                      ],
#                          'value': relevance
#                          },
#                         {'name': 'offset_divergence',
#                          'value': float(divergence)}],
#             'op': 'prod',
#             'value': float(score.value)
#         })
#         return score