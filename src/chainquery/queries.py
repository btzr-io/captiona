from pypika import Query, Order, Criterion, functions as fn

#  local modules
from .tables import claim
from .constants import CLAIM_TYPE, CONTENT_TYPE


def getStreamClaim(claim_id, channel_id, mime_type, language):
    # Basic query
    q =  Query.from_(claim).select(
        claim.name,
        claim.claim_id,
        claim.language,
        claim.publisher_id
    ).where(
        flag_mime_type(mime_type) & flag_linked_claim(claim_id, language)
    )

    # Published by channel
    if channel_id:
        q = q.where(claim.publisher_id == channel_id)

    # Published by channel
    if channel_id:
        q = q.where(claim.language == language)

    # returns new query
    return q

def flag_linked_claim(id, lang):
    # Linked by id and content languge
    if id and lang:
        return claim.name == lang + '_' + id
    # Linked by id only
    return claim.name.like('%' + '_' + id)

def flag_mime_type(mime_type):
    return Criterion.all([
        claim.type == CLAIM_TYPE['STREAM'],
        claim.content_type == mime_type
    ])


# flags
def  flag_licensed_content():
    return Criterion.all([
        claim.license != "",
        claim.license.notnull(),
        claim.publisher_id.notnull()
    ])

def  flag_unlicensed_content():
    return Criterion.any([
        claim.license == "",
        claim.license.isnull(),
    ])

def flag_content_type(content_type):
    return Criterion.all([
        claim.type == CLAIM_TYPE['STREAM'],
        claim.content_type.like(content_type + '%')
    ])

def flag_audio_duration():
    return Criterion.all([
        claim.audio_duration.notnull(),
        claim.audio_duration > 0
    ])

def flag_active_claim():
    return Criterion.all([
    claim.bid_state.notnull(),
    claim.bid_state != 'Spent',
    claim.bid_state != 'Expired',
    claim.bid_state != 'Accepted'
    ])
#---------------- #
#  Useful queries #
# --------------- #

def byContentType(contentType):
    # Basic query
    q =  Query.from_(claim).select(
        claim.title,
        claim.claim_id,
        claim.content_type,
        #'*'
    ).where(
        flag_content_type(CONTENT_TYPE['AUDIO']) & flag_licensed_content() & flag_audio_duration()  & flag_active_claim()
    )
    # returns new query
    return q


def contentType(contentType):
    # Basic query
    q =  Query.from_(claim).select(
        claim.content_type,
        fn.Count(claim.content_type).as_("total")
    ).where(
        flag_content_type(CONTENT_TYPE['AUDIO']) & flag_audio_duration()  & flag_active_claim()
    )
    # returns new query
    return q

def contentType(contentType):
    # Basic query
    q =  Query.from_(claim).select(
        claim.content_type,
        fn.Count(claim.content_type).as_("total")
    ).where(
        flag_content_type(CONTENT_TYPE['AUDIO']) & flag_audio_duration()  & flag_active_claim()
    )
    # returns new query
    return q


def audioDuration():
    # Basic query
    q =  Query.from_(claim).select(
        fn.Avg(claim.audio_duration).as_('avg'),
        fn.Max(claim.audio_duration).as_('max'),
        fn.Min(claim.audio_duration).as_('min'),
        fn.Sum(claim.audio_duration).as_('sum')
    ).where(
        flag_content_type(CONTENT_TYPE['AUDIO']) & flag_audio_duration() & flag_active_claim()
    )
    # returns new query
    return q




def contentAudio():
    return byContentType(CONTENT_TYPE['AUDIO'])

def contentAudioTypes():
    return contentType(CONTENT_TYPE['AUDIO']).groupby(claim.content_type).orderby(fn.Count(claim.content_type), order=Order.desc)


    # regex tags
    # (^[a-zA-Z][\w_-]+)
