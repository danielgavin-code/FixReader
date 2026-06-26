import re
from markupsafe import Markup, escape


def _strip_html(s):
    """Remove HTML tags and return plain text. Decode entities before stripping
    so that entity-encoded tags (e.g. &lt;strong&gt;) are also removed."""
    s = str(s)
    s = s.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&nbsp;', ' ')
    return re.sub(r'<[^>]*>', '', s)

# ── Tag definitions ────────────────────────────────────────────────────────────
TAGS = {
    1:   ('Account',               'Account mnemonic as agreed between buy and sell sides',                      'String'),
    6:   ('AvgPx',                 'Calculated average price of all fills on this order',                        'Price'),
    8:   ('BeginString',           'Identifies beginning of new message and protocol version',                   'String'),
    9:   ('BodyLength',            'Message length in bytes, forward to the CheckSum field',                     'Length'),
    10:  ('CheckSum',              'Three-digit modulo-256 checksum of all bytes up to this field',              'String'),
    11:  ('ClOrdID',               'Unique identifier for order as assigned by the buy-side (client)',           'String'),
    14:  ('CumQty',                'Total quantity (shares) filled',                                             'Qty'),
    15:  ('Currency',              'Currency used for price (ISO 4217)',                                         'Currency'),
    17:  ('ExecID',                'Unique identifier of execution message assigned by sell-side',               'String'),
    18:  ('ExecInst',              'Instructions for order handling on broker trading floor',                    'MultipleValueString'),
    21:  ('HandlInst',             'Instructions for order handling on the broker trading floor',                'char'),
    22:  ('SecurityIDSource',      'Identifies the class or source of the SecurityID value',                    'String'),
    30:  ('LastMkt',               'Market of execution for the last fill',                                     'Exchange'),
    31:  ('LastPx',                'Price of the last fill',                                                    'Price'),
    32:  ('LastQty',               'Quantity bought or sold on this fill',                                      'Qty'),
    34:  ('MsgSeqNum',             'Integer message sequence number',                                           'SeqNum'),
    35:  ('MsgType',               'Defines message type — ALWAYS the second tag in the message',               'String'),
    37:  ('OrderID',               'Unique identifier for order as assigned by the sell-side (broker)',          'String'),
    38:  ('OrderQty',              'Quantity ordered, expressed in units (shares)',                              'Qty'),
    39:  ('OrdStatus',             'Identifies current status of order',                                        'char'),
    40:  ('OrdType',               'Order type',                                                                'char'),
    41:  ('OrigClOrdID',           'ClOrdID of the previous order (used in cancel/replace requests)',            'String'),
    43:  ('PossDupFlag',           'Indicates possible retransmission of message with this sequence number',     'Boolean'),
    44:  ('Price',                 'Price per unit of quantity (for limit orders)',                              'Price'),
    45:  ('RefSeqNum',             'Reference message sequence number',                                         'SeqNum'),
    48:  ('SecurityID',            'Security identifier value of the type specified by SecurityIDSource',       'String'),
    49:  ('SenderCompID',          'Assigned value used to identify the firm sending this message',             'String'),
    50:  ('SenderSubID',           'Assigned value to identify specific message originator (desk, trader)',      'String'),
    52:  ('SendingTime',           'Time of message transmission (always UTC, format: YYYYMMDD-HH:MM:SS)',      'UTCTimestamp'),
    54:  ('Side',                  'Side of order',                                                             'char'),
    55:  ('Symbol',                'Ticker symbol — common, human-understood representation of the security',   'String'),
    56:  ('TargetCompID',          'Assigned value used to identify the firm receiving this message',           'String'),
    57:  ('TargetSubID',           'Assigned value to identify specific individual or unit intended to receive','String'),
    58:  ('Text',                  'Free format text string (may be encrypted)',                                'String'),
    60:  ('TransactTime',          'Time of execution/order creation in UTC',                                   'UTCTimestamp'),
    97:  ('PossResend',            'Indicates that message may contain information from a prior send attempt',  'Boolean'),
    98:  ('EncryptMethod',         'Method of encryption used',                                                 'int'),
    99:  ('StopPx',                'Price per unit of quantity for stop orders',                                'Price'),
    100: ('ExDestination',         'Execution destination (market/exchange identifier)',                        'Exchange'),
    103: ('OrdRejReason',          'Code to identify reason for order rejection',                               'int'),
    107: ('SecurityDesc',          'Security description',                                                      'String'),
    108: ('HeartBtInt',            'Heartbeat interval in seconds',                                             'int'),
    109: ('ClientID',              'Firm identifier used in third-party transaction reporting',                 'String'),
    110: ('MinQty',                'Minimum quantity of an order to be executed',                               'Qty'),
    111: ('MaxFloor',              'Maximum number of shares to be shown on the floor at any given time',      'Qty'),
    112: ('TestReqID',             'Identifier included in Test Request message; echoed back in Heartbeat',    'String'),
    113: ('ReportToExch',          'Indicates party responsible for transaction reporting to the exchange',    'Boolean'),
    114: ('LocateReqd',            'Indicates whether the broker is to locate the stock in advance of short sale', 'Boolean'),
    115: ('OnBehalfOfCompID',      'Assigned value to identify the firm on whose behalf a message is sent',   'String'),
    116: ('OnBehalfOfSubID',       'On behalf of sub-identifier',                                              'String'),
    122: ('OrigSendingTime',       'Original time of message transmission for retransmitted messages',         'UTCTimestamp'),
    128: ('DeliverToCompID',       'Assigned value for the firm the message should be delivered to',           'String'),
    131: ('QuoteReqID',            'Unique identifier for quote request',                                      'String'),
    132: ('BidPx',                 'Bid price/rate',                                                           'Price'),
    133: ('OfferPx',               'Offer price/rate',                                                         'Price'),
    134: ('BidSize',               'Quantity of bid',                                                          'Qty'),
    135: ('OfferSize',             'Quantity of offer',                                                        'Qty'),
    141: ('ResetSeqNumFlag',       'Indicates both sides of the FIX session should reset sequence numbers',   'Boolean'),
    142: ('SenderLocationID',      'Assigned value to identify specific message originator location',         'String'),
    143: ('TargetLocationID',      'Assigned value to identify specific individual, unit, or location',       'String'),
    150: ('ExecType',              'Describes the specific Execution Report (e.g. New, Fill, Rejected)',      'char'),
    151: ('LeavesQty',             'Quantity open for further execution. LeavesQty = OrderQty − CumQty',     'Qty'),
    167: ('SecurityType',          'Indicates type of security (CS=Common Stock, FUT=Futures, OPT=Options)', 'String'),
    207: ('SecurityExchange',      'Market used to help identify a security',                                  'Exchange'),
    210: ('MaxShow',               'Maximum quantity to be shown to other customers at any given time',       'Qty'),
    211: ('PegOffsetValue',        'Amount (absolute or relative) the order is pegged at',                   'float'),
    262: ('MDReqID',               'Unique identifier for Market Data Request',                               'String'),
    263: ('SubscriptionRequestType','Type of Market Data request',                                            'char'),
    264: ('MarketDepth',           'Depth of market for book snapshot (0 = full book)',                      'int'),
    267: ('NoMDEntryTypes',        'Number of MDEntryType fields requested',                                  'NumInGroup'),
    268: ('NoMDEntries',           'Number of entries in Market Data message',                                'NumInGroup'),
    269: ('MDEntryType',           'Type of Market Data entry',                                              'char'),
    270: ('MDEntryPx',             'Price of the Market Data entry',                                         'Price'),
    271: ('MDEntrySize',           'Quantity or volume represented by the Market Data entry',                'Qty'),
    279: ('MDUpdateAction',        'Type of Market Data update action',                                      'char'),
    336: ('TradingSessionID',      'Identifier for Trading Session (e.g. DAY, PRE, POST)',                  'String'),
    371: ('RefTagID',              'Tag number of the FIX field being referenced in a Reject',               'int'),
    372: ('RefMsgType',            'MsgType of the FIX message being referenced in a Business Reject',      'String'),
    373: ('SessionRejectReason',   'Code to identify reason for a session-level Reject message',             'int'),
    375: ('ContraBroker',          'Contra broker identifier',                                               'String'),
    376: ('ComplianceID',          'Identifier used for regulatory compliance reporting purposes',            'String'),
    377: ('SolicitedFlag',         'Indicates whether the order was solicited by the broker',                'Boolean'),
    378: ('ExecRestatementReason', 'Code to identify reason for an Execution Report restatement',           'int'),
    379: ('BusinessRejectRefID',   'Value to which a Business Message Reject refers',                       'String'),
    380: ('BusinessRejectReason',  'Code to identify reason for a Business Message Reject',                 'int'),
    381: ('GrossTradeAmt',         'Total amount traded in units of currency (Price × Qty)',                'Amt'),
    382: ('NoContraBrokers',       'Number of ContraBroker entries in repeating group',                    'NumInGroup'),
}

# ── Enum values for common tags ────────────────────────────────────────────────
ENUMS = {
    35: {
        '0': 'Heartbeat',
        '1': 'Test Request',
        '2': 'Resend Request',
        '3': 'Reject',
        '4': 'Sequence Reset',
        '5': 'Logout',
        '6': 'Indication of Interest',
        '7': 'Advertisement',
        '8': 'Execution Report',
        '9': 'Order Cancel Reject',
        'A': 'Logon',
        'B': 'News',
        'C': 'Email',
        'D': 'New Order — Single',
        'E': 'New Order — List',
        'F': 'Order Cancel Request',
        'G': 'Order Cancel/Replace Request',
        'H': 'Order Status Request',
        'J': 'Allocation Instruction',
        'K': 'List Cancel Request',
        'L': 'List Execute',
        'M': 'List Status Request',
        'N': 'List Status',
        'P': 'Allocation Instruction Ack',
        'Q': "Don't Know Trade",
        'R': 'Quote Request',
        'S': 'Quote',
        'T': 'Settlement Instructions',
        'V': 'Market Data Request',
        'W': 'Market Data — Snapshot/Full Refresh',
        'X': 'Market Data — Incremental Refresh',
        'Y': 'Market Data Request Reject',
        'Z': 'Quote Cancel',
        'a': 'Quote Status Report',
        'b': 'Quote Acknowledgement',
        'c': 'Security Definition Request',
        'd': 'Security Definition',
        'e': 'Security Status Request',
        'f': 'Security Status',
        'g': 'Trading Session Status Request',
        'h': 'Trading Session Status',
        'i': 'Mass Quote',
        'j': 'Business Message Reject',
        'k': 'Bid Request',
        'l': 'Bid Response',
        'm': 'List Strike Price',
    },
    54: {
        '1': 'Buy',
        '2': 'Sell',
        '3': 'Buy Minus',
        '4': 'Sell Plus',
        '5': 'Sell Short',
        '6': 'Sell Short Exempt',
        '7': 'Undisclosed',
        '8': 'Cross',
        '9': 'Cross Short',
        'A': 'Cross Short Exempt',
        'B': 'As Defined',
        'C': 'Opposite',
    },
    40: {
        '1': 'Market',
        '2': 'Limit',
        '3': 'Stop',
        '4': 'Stop Limit',
        '5': 'Market On Close',
        '6': 'With Or Without',
        '7': 'Limit Or Better',
        '8': 'Limit With Or Without',
        '9': 'On Basis',
        'D': 'Previously Quoted',
        'E': 'Previously Indicated',
        'I': 'Funari',
        'J': 'Market If Touched',
        'K': 'Market With Left Over as Limit',
        'P': 'Pegged',
    },
    39: {
        '0': 'New',
        '1': 'Partially Filled',
        '2': 'Filled',
        '3': 'Done For Day',
        '4': 'Canceled',
        '5': 'Replaced',
        '6': 'Pending Cancel',
        '7': 'Stopped',
        '8': 'Rejected',
        '9': 'Suspended',
        'A': 'Pending New',
        'B': 'Calculated',
        'C': 'Expired',
        'D': 'Accepted For Bidding',
        'E': 'Pending Replace',
    },
    150: {
        '0': 'New',
        '1': 'Partial Fill',
        '2': 'Fill',
        '3': 'Done For Day',
        '4': 'Canceled',
        '5': 'Replace',
        '6': 'Pending Cancel',
        '7': 'Stopped',
        '8': 'Rejected',
        '9': 'Suspended',
        'A': 'Pending New',
        'B': 'Calculated',
        'C': 'Expired',
        'D': 'Restated',
        'E': 'Pending Replace',
        'F': 'Trade (Partial Fill or Fill)',
        'G': 'Trade Correct',
        'H': 'Trade Cancel',
        'I': 'Order Status',
    },
    21: {
        '1': 'Automated execution, private (no broker intervention)',
        '2': 'Automated execution, public (broker intervention OK)',
        '3': 'Manual order, best execution',
    },
    43: {'Y': 'Yes — possible duplicate', 'N': 'No — original transmission'},
    97: {'Y': 'Yes — possible resend', 'N': 'No — original send'},
    98: {
        '0': 'None / Cleartext',
        '1': 'PKCS (Proprietary)',
        '2': 'DES (ECB Mode)',
        '3': 'PKCS/DES (Proprietary)',
        '4': 'PGP/DES (Defunct)',
        '5': 'PGP/DES-MD5 (Defunct)',
        '6': 'PEM/DES-MD5 (Defunct)',
    },
    103: {
        '0': 'Broker/Exchange Option',
        '1': 'Unknown Symbol',
        '2': 'Exchange Closed',
        '3': 'Order Exceeds Limit',
        '4': 'Too Late to Enter',
        '5': 'Unknown Order',
        '6': 'Duplicate Order',
        '7': 'Duplicate of a Verbally Communicated Order',
        '8': 'Stale Order',
        '9': 'Trade Along Required',
        '10': 'Invalid Investor ID',
        '11': 'Unsupported Order Characteristic',
        '12': 'Surveillance Option',
        '13': 'Incorrect Quantity',
        '14': 'Incorrect Allocated Quantity',
        '15': 'Unknown Account',
        '99': 'Other',
    },
    113: {'Y': 'Sell-side reports to exchange', 'N': 'Buy-side reports to exchange'},
    114: {'Y': 'Locate required', 'N': 'Locate not required'},
    141: {'Y': 'Yes — reset seq nums to 1', 'N': 'No — maintain seq nums'},
    263: {
        '0': 'Snapshot only',
        '1': 'Snapshot + Updates (Subscribe)',
        '2': 'Unsubscribe (Disable previous request)',
    },
    269: {
        '0': 'Bid',
        '1': 'Offer',
        '2': 'Trade',
        '3': 'Index Value',
        '4': 'Opening Price',
        '5': 'Closing Price',
        '6': 'Settlement Price',
        '7': 'Trading Session High Price',
        '8': 'Trading Session Low Price',
        '9': 'Trading Session VWAP Price',
        'A': 'Imbalance',
        'B': 'Trade Volume',
        'C': 'Open Interest',
    },
    279: {'0': 'New', '1': 'Change', '2': 'Delete'},
    373: {
        '0': 'Invalid Tag Number',
        '1': 'Required Tag Missing',
        '2': 'Tag Not Defined For This Message Type',
        '3': 'Undefined Tag',
        '4': 'Tag Specified Without a Value',
        '5': 'Value Is Incorrect (Out of Range)',
        '6': 'Incorrect Data Format for Value',
        '7': 'Decryption Problem',
        '8': 'Signature Problem',
        '9': 'CompID Problem',
        '10': 'SendingTime Accuracy Problem',
        '11': 'Invalid MsgType',
        '12': 'XML Validation Error',
        '13': 'Tag Appears More Than Once',
        '14': 'Tag Specified Out of Required Order',
        '99': 'Other',
    },
    377: {'Y': 'Order was solicited', 'N': 'Order was not solicited'},
    380: {
        '0': 'Application not available',
        '1': 'Conditionally required field missing',
        '2': 'Not authorized / permissions denied',
        '3': 'Unknown ID',
        '4': 'Unknown Security',
        '5': 'Unsupported Message Type',
        '6': 'Not subscribed to that data',
        '7': 'Usage limit hit',
        '99': 'Other',
    },
}

# Tags that form the session header / trailer (rendered differently in the table)
HEADER_TAGS  = {8, 9, 34, 35, 43, 49, 50, 52, 56, 57, 97, 115, 116, 122, 128, 142, 143}
TRAILER_TAGS = {10}

# Row highlight classes for important tags (Side handled separately in decode_fix)
HIGHLIGHT_TAGS = {
    8: 'hl-session', 9: 'hl-session', 34: 'hl-session',
    35: 'hl-msgtype',
    43: 'hl-session', 49: 'hl-session', 50: 'hl-session',
    52: 'hl-session', 56: 'hl-session', 57: 'hl-session',
    55: 'hl-symbol',
    38: 'hl-qty', 32: 'hl-qty', 14: 'hl-qty', 151: 'hl-qty',
    44: 'hl-price', 31: 'hl-price', 6: 'hl-price',
    39: 'hl-status', 150: 'hl-status',
    10: 'hl-trailer',
}


# ── Core decode function ───────────────────────────────────────────────────────
def decode_fix(raw_message):
    raw = (raw_message or '').strip()
    if not raw:
        return [], 'empty'

    delimiter = '\x01' if '\x01' in raw else '|'
    parts = raw.split(delimiter)

    fields = []
    for part in parts:
        part = part.strip()
        if not part or '=' not in part:
            continue
        tag_str, _, value = part.partition('=')
        tag_str = tag_str.strip()
        value   = value.strip()
        try:
            tag_num = int(tag_str)
        except ValueError:
            continue

        tag_data = TAGS.get(tag_num)
        if tag_data:
            name, desc, type_ = tag_data
        else:
            name  = f'Tag {tag_num}'
            desc  = 'Custom or unrecognized tag — may be a vendor extension'
            type_ = 'Unknown'

        enum_val = ENUMS.get(tag_num, {}).get(value)
        section  = 'header' if tag_num in HEADER_TAGS else ('trailer' if tag_num in TRAILER_TAGS else 'body')
        if tag_num == 54:
            highlight = 'hl-side-buy' if value == '1' else ('hl-side-sell' if value == '2' else 'hl-side')
        else:
            highlight = HIGHLIGHT_TAGS.get(tag_num, '')

        fields.append({
            'tag':        tag_num,
            'name':       name,
            'value':      value,
            'enum_value': enum_val,
            'description': desc,
            'type':       type_,
            'section':    section,
            'highlight':  highlight,
        })

    if not fields:
        return [], 'invalid'
    return fields, 'ok'


# ── Summary generator ──────────────────────────────────────────────────────────
def _safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0


def generate_summary(fields):
    if not fields:
        return None

    fm = {f['tag']: f for f in fields}

    def raw(tag):
        f = fm.get(tag)
        return f['value'] if f else None

    def decoded(tag):
        f = fm.get(tag)
        if not f:
            return None
        return f['enum_value'] or f['value']

    msg_type_val  = raw(35) or ''
    msg_type_name = decoded(35) or 'Unknown'
    fix_version   = raw(8)  or 'Unknown'
    sender        = raw(49) or '—'
    target        = raw(56) or '—'
    seq_num       = raw(34) or '—'
    sending_time  = raw(52) or '—'

    narrative  = []
    key_facts  = []

    def e(val):
        return escape(val) if val else '—'

    if msg_type_val == 'D':
        symbol    = raw(55) or '?'
        side      = decoded(54) or raw(54) or '?'
        qty       = raw(38) or '?'
        ord_type  = decoded(40) or '?'
        price     = raw(44)
        acct      = raw(1)
        cl_ord_id = raw(11)

        narrative.append(Markup(
            f'<strong>{e(sender)}</strong> is submitting a '
            f'<strong>{e(side)}</strong> order for '
            f'<strong>{e(qty)} shares</strong> of <strong>{e(symbol)}</strong>.'
        ))
        if ord_type == 'Limit' and price:
            narrative.append(Markup(
                f'Order type is <strong>Limit</strong> at a price of <strong>${e(price)}</strong> per share.'
            ))
        elif ord_type != '?':
            narrative.append(Markup(f'Order type: <strong>{e(ord_type)}</strong>.'))
        if acct:
            narrative.append(Markup(f'Account: <code>{e(acct)}</code>.'))
        if cl_ord_id:
            narrative.append(Markup(f'Client order ID (ClOrdID): <code>{e(cl_ord_id)}</code>.'))

        key_facts = [
            ('Symbol',     symbol),
            ('Side',       side),
            ('Quantity',   qty),
            ('Order Type', ord_type),
            ('Price',      f'${price}' if price else '—'),
        ]

    elif msg_type_val == '8':
        ord_status  = decoded(39) or '?'
        exec_type   = decoded(150) or '?'
        symbol      = raw(55) or '?'
        side        = decoded(54) or raw(54) or ''
        cum_qty     = raw(14) or '0'
        leaves_qty  = raw(151) or '?'
        last_px     = raw(31)
        last_qty    = raw(32) or '0'
        avg_px      = raw(6) or '—'
        ord_id      = raw(37)

        narrative.append(Markup(
            f'Execution Report from <strong>{e(sender)}</strong> to <strong>{e(target)}</strong>'
            f'{(" for <strong>" + e(symbol) + "</strong>") if symbol != "?" else ""}.'
        ))
        narrative.append(Markup(
            f'Order status: <strong>{e(ord_status)}</strong>. '
            f'Execution type: <strong>{e(exec_type)}</strong>.'
        ))
        if _safe_float(last_qty) > 0 and last_px:
            narrative.append(Markup(
                f'Last fill: <strong>{e(last_qty)} shares at ${e(last_px)}</strong>.'
            ))
        narrative.append(Markup(
            f'Cumulative filled: <strong>{e(cum_qty)}</strong> &nbsp;|&nbsp; '
            f'Remaining (LeavesQty): <strong>{e(leaves_qty)}</strong> &nbsp;|&nbsp; '
            f'Avg price: <strong>${avg_px}</strong>.'
        ))
        if ord_id:
            narrative.append(Markup(f'Sell-side order ID (OrderID): <code>{e(ord_id)}</code>.'))

        key_facts = [
            ('Symbol',    symbol),
            ('Side',      side if side else '—'),
            ('Ord Status', ord_status),
            ('Exec Type', exec_type),
            ('Filled',    cum_qty),
            ('Remaining', leaves_qty),
            ('Avg Price', f'${avg_px}'),
        ]

    elif msg_type_val == '0':
        test_req = raw(112)
        narrative.append(Markup(
            f'<strong>Heartbeat</strong> from <strong>{e(sender)}</strong> to <strong>{e(target)}</strong>.'
        ))
        narrative.append(Markup(
            'Heartbeats are sent at regular intervals to verify that the FIX session is '
            'still active. No trading action is implied.'
        ))
        if test_req:
            narrative.append(Markup(
                f'This Heartbeat is responding to Test Request ID: <code>{e(test_req)}</code>.'
            ))

    elif msg_type_val == 'A':
        heartbt = raw(108) or '—'
        reset   = raw(141)
        enc     = decoded(98)
        narrative.append(Markup(
            f'<strong>Logon</strong> from <strong>{e(sender)}</strong> to <strong>{e(target)}</strong> '
            f'— the first message that establishes a FIX session.'
        ))
        narrative.append(Markup(
            f'Heartbeat interval: <strong>{e(heartbt)} seconds</strong>. '
            f'Both sides must successfully exchange Logon messages before any orders can be sent.'
        ))
        if reset == 'Y':
            narrative.append(Markup(
                'Sequence number reset requested — both sides will reset to SeqNum 1.'
            ))
        if enc:
            narrative.append(Markup(f'Encryption: {e(enc)}.'))

        key_facts = [
            ('HeartBtInt',   f'{heartbt}s'),
            ('ResetSeqNums', decoded(141) or '—'),
            ('Encrypt',      enc or 'None'),
        ]

    elif msg_type_val == '5':
        text = raw(58)
        narrative.append(Markup(
            f'<strong>Logout</strong> from <strong>{e(sender)}</strong> to <strong>{e(target)}</strong>.'
        ))
        narrative.append(Markup(
            'Logout gracefully terminates the FIX session. The receiving side should '
            'respond with its own Logout before closing the connection.'
        ))
        if text:
            narrative.append(Markup(f'Reason: “{e(text)}”'))

    elif msg_type_val == 'F':
        orig = raw(41) or '?'
        symbol = raw(55) or '?'
        side   = decoded(54) or raw(54) or '?'
        narrative.append(Markup(
            f'<strong>{e(sender)}</strong> is requesting cancellation of an order for '
            f'<strong>{e(symbol)}</strong> (<strong>{e(side)}</strong> side).'
        ))
        narrative.append(Markup(
            f'The original client order ID being cancelled: <code>{e(orig)}</code>. '
            'A Cancel Reject will be sent back if the order cannot be cancelled.'
        ))
        key_facts = [
            ('Symbol',      symbol),
            ('Side',        side),
            ('OrigClOrdID', orig),
            ('New ClOrdID', raw(11) or '—'),
        ]

    elif msg_type_val == 'G':
        symbol = raw(55) or '?'
        side   = decoded(54) or raw(54) or '?'
        qty    = raw(38) or '?'
        price  = raw(44)
        orig   = raw(41) or '?'
        narrative.append(Markup(
            f'<strong>{e(sender)}</strong> is requesting to <strong>amend</strong> an existing '
            f'order for <strong>{e(symbol)}</strong>.'
        ))
        if price:
            narrative.append(Markup(
                f'New parameters: {e(side)} <strong>{e(qty)} shares</strong> at <strong>${e(price)}</strong>.'
            ))
        narrative.append(Markup(
            f'Original ClOrdID being replaced: <code>{e(orig)}</code>.'
        ))
        key_facts = [
            ('Symbol',      symbol),
            ('Side',        side),
            ('New Qty',     qty),
            ('New Price',   f'${price}' if price else '—'),
            ('OrigClOrdID', orig),
        ]

    elif msg_type_val == '3':
        ref_seq = raw(45) or '?'
        reason  = decoded(373) or raw(373) or '?'
        text    = raw(58)
        narrative.append(Markup(
            f'<strong>Session-level Reject</strong> — message sequence #{e(ref_seq)} was rejected.'
        ))
        narrative.append(Markup(f'Reason: <strong>{e(reason)}</strong>.'))
        if text:
            narrative.append(Markup(f'Details: “{e(text)}”'))

    elif msg_type_val == '9':
        cl_ord_id  = raw(11) or '?'
        ord_status = decoded(39) or '?'
        narrative.append(Markup(
            f'<strong>Order Cancel Reject</strong> — the cancel or replace request for '
            f'<code>{e(cl_ord_id)}</code> was <strong>rejected</strong>.'
        ))
        narrative.append(Markup(
            f'Current order status: <strong>{e(ord_status)}</strong>. '
            'The original order remains in effect.'
        ))

    elif msg_type_val == 'H':
        symbol    = raw(55) or '?'
        cl_ord_id = raw(11) or '?'
        narrative.append(Markup(
            f'<strong>{e(sender)}</strong> is requesting the current status of order '
            f'<code>{e(cl_ord_id)}</code>'
            f'{(" for " + "<strong>" + e(symbol) + "</strong>") if symbol != "?" else ""}.'
        ))
        narrative.append(Markup(
            'The broker will respond with an Execution Report (35=8) reflecting the '
            'current OrdStatus of the order.'
        ))

    elif msg_type_val in ('V', 'W', 'X', 'Y'):
        symbol = raw(55) or 'multiple instruments'
        narrative.append(Markup(
            f'<strong>{e(msg_type_name)}</strong> message'
            f' for <strong>{e(symbol)}</strong>.'
        ))
        if msg_type_val == 'V':
            sub = decoded(263) or '?'
            narrative.append(Markup(f'Subscription type: <strong>{e(sub)}</strong>.'))

    else:
        narrative.append(Markup(
            f'<strong>{e(msg_type_name)}</strong> message from '
            f'<strong>{e(sender)}</strong> to <strong>{e(target)}</strong>.'
        ))

    summary_fields = _build_summary_fields(msg_type_val, fm)
    key_takeaways  = _build_key_takeaways(msg_type_val, fm)

    return {
        'msg_type_val':   msg_type_val,
        'msg_type_name':  msg_type_name,
        'fix_version':    fix_version,
        'sender':         sender,
        'target':         target,
        'seq_num':        seq_num,
        'sending_time':   sending_time,
        'narrative':      [_strip_html(n) for n in narrative],
        'key_facts':      [(k, v) for k, v in key_facts if v and v != '—'],
        'category':       _msg_category(msg_type_val),
        'summary_fields': summary_fields,
        'key_takeaways':  key_takeaways,
    }


def _msg_category(t):
    if t in {'D', 'E', 'F', 'G', 'H', 'K', 'L', 'M', 'N'}:
        return 'order'
    if t in {'8', '9', 'J', 'P'}:
        return 'execution'
    if t in {'0', '1', '2', '3', '4', '5', 'A'}:
        return 'session'
    if t in {'V', 'W', 'X', 'Y'}:
        return 'market-data'
    if t in {'R', 'S', 'Z', 'a', 'b', 'i'}:
        return 'quote'
    return 'other'


# ── Summary fields for the MESSAGE SUMMARY panel ───────────────────────────────
def _build_summary_fields(msg_type_val, fm):
    def r(tag):
        f = fm.get(tag); return f['value'] if f else None
    def d(tag):
        f = fm.get(tag); return (f['enum_value'] or f['value']) if f else None

    def side_style(val):
        return 'val-buy' if val == '1' else ('val-sell' if val == '2' else '')

    side_raw = r(54)

    if msg_type_val == 'D':
        price = r(44)
        return [
            {'icon': 'symbol', 'label': 'Symbol',     'value': r(55) or '—',                    'style': ''},
            {'icon': 'side',   'label': 'Side',        'value': d(54) or side_raw or '—',        'style': side_style(side_raw)},
            {'icon': 'type',   'label': 'Order Type',  'value': d(40) or r(40) or '—',           'style': ''},
            {'icon': 'qty',    'label': 'Quantity',    'value': (r(38) + ' shs') if r(38) else '—', 'style': ''},
            {'icon': 'price',  'label': 'Price',       'value': f'${price}' if price else '—',   'style': 'val-price' if price else ''},
        ]
    elif msg_type_val == '8':
        avg = r(6); show_avg = avg and avg not in ('0', '0.00', '0.0')
        return [
            {'icon': 'symbol', 'label': 'Symbol',          'value': r(55) or '—',                          'style': ''},
            {'icon': 'side',   'label': 'Side',             'value': d(54) or side_raw or '—',              'style': side_style(side_raw)},
            {'icon': 'status', 'label': 'Ord Status',       'value': d(39) or r(39) or '—',                 'style': ''},
            {'icon': 'qty',    'label': 'Filled / Leaves',  'value': f"{r(14) or '0'} / {r(151) or '?'}",  'style': ''},
            {'icon': 'price',  'label': 'Avg Price',        'value': f'${avg}' if show_avg else '—',        'style': 'val-price' if show_avg else ''},
        ]
    elif msg_type_val in ('F', 'G'):
        price = r(44)
        fields = [
            {'icon': 'symbol', 'label': 'Symbol',      'value': r(55) or '—',   'style': ''},
            {'icon': 'side',   'label': 'Side',         'value': d(54) or side_raw or '—', 'style': side_style(side_raw)},
            {'icon': 'orig',   'label': 'OrigClOrdID', 'value': r(41) or '—',   'style': ''},
            {'icon': 'id',     'label': 'New ClOrdID', 'value': r(11) or '—',   'style': ''},
        ]
        if msg_type_val == 'G':
            fields.append({'icon': 'qty',   'label': 'New Qty',   'value': r(38) or '—',          'style': ''})
            if price:
                fields.append({'icon': 'price', 'label': 'New Price', 'value': f'${price}', 'style': 'val-price'})
        return fields
    elif msg_type_val == 'A':
        hb = r(108)
        return [
            {'icon': 'session', 'label': 'From',         'value': r(49) or '—',              'style': ''},
            {'icon': 'session', 'label': 'To',           'value': r(56) or '—',              'style': ''},
            {'icon': 'time',    'label': 'Heartbeat',    'value': f'{hb}s' if hb else '—',   'style': ''},
            {'icon': 'reset',   'label': 'Reset SeqNums','value': d(141) or r(141) or '—',   'style': ''},
            {'icon': 'enc',     'label': 'Encryption',   'value': d(98) or r(98) or '—',     'style': ''},
        ]
    elif msg_type_val == '0':
        return [
            {'icon': 'session', 'label': 'From',    'value': r(49) or '—', 'style': ''},
            {'icon': 'session', 'label': 'To',      'value': r(56) or '—', 'style': ''},
            {'icon': 'seq',     'label': 'Seq #',   'value': r(34) or '—', 'style': ''},
            {'icon': 'time',    'label': 'Sent At', 'value': r(52) or '—', 'style': ''},
        ]
    elif msg_type_val == '5':
        return [
            {'icon': 'session', 'label': 'From',   'value': r(49) or '—', 'style': ''},
            {'icon': 'session', 'label': 'To',     'value': r(56) or '—', 'style': ''},
            {'icon': 'text',    'label': 'Reason', 'value': r(58) or '—', 'style': ''},
        ]
    elif msg_type_val in ('V', 'W', 'X'):
        return [
            {'icon': 'symbol',  'label': 'Symbol',   'value': r(55) or '—', 'style': ''},
            {'icon': 'session', 'label': 'From',     'value': r(49) or '—', 'style': ''},
            {'icon': 'session', 'label': 'To',       'value': r(56) or '—', 'style': ''},
            {'icon': 'seq',     'label': 'MDReqID',  'value': r(262) or '—', 'style': ''},
        ]
    else:
        return [
            {'icon': 'session', 'label': 'From',     'value': r(49) or '—',         'style': ''},
            {'icon': 'session', 'label': 'To',       'value': r(56) or '—',         'style': ''},
            {'icon': 'msg',     'label': 'Msg Type', 'value': d(35) or r(35) or '—','style': ''},
            {'icon': 'seq',     'label': 'Seq #',    'value': r(34) or '—',         'style': ''},
        ]


# ── Key takeaways for the right sidebar ───────────────────────────────────────
def _build_key_takeaways(msg_type_val, fm):
    def r(tag):
        f = fm.get(tag); return f['value'] if f else None

    if msg_type_val == 'D':
        return [
            {'color': 'blue',   'text': 'Tag 35=D identifies this as a New Order — Single, the most common FIX message type.'},
            {'color': 'green',  'text': 'ClOrdID (11) must be unique within a session — it is your order tracking reference.'},
            {'color': 'orange', 'text': 'Price (44) is only required for Limit orders (OrdType=2). Market orders omit it.'},
            {'color': 'purple', 'text': 'HandlInst (21) tells the broker how to handle the order on the trading floor.'},
            {'color': 'gray',   'text': 'CheckSum (10) = sum of all byte values mod 256, zero-padded to 3 digits.'},
        ]
    elif msg_type_val == '8':
        return [
            {'color': 'blue',   'text': 'ExecType (150) describes this specific report; OrdStatus (39) reflects the overall order state.'},
            {'color': 'green',  'text': 'A fill has ExecType=F. A new-order acknowledgment has ExecType=0 (New).'},
            {'color': 'orange', 'text': 'LeavesQty (151) = OrderQty (38) − CumQty (14). Must be zero when order is complete.'},
            {'color': 'purple', 'text': 'ExecID (17) is assigned by the sell-side and must be unique per execution event.'},
            {'color': 'blue',   'text': 'OrderID (37) is the broker\'s ID; ClOrdID (11) is the client\'s ID for the same order.'},
        ]
    elif msg_type_val == '0':
        return [
            {'color': 'blue',   'text': 'Heartbeats are sent if HeartBtInt seconds pass without any other message.'},
            {'color': 'green',  'text': 'If responding to a Test Request (35=1), must echo the TestReqID (112) back.'},
            {'color': 'orange', 'text': 'Missed heartbeat → Test Request → no response → Logout. This is the standard recovery flow.'},
            {'color': 'purple', 'text': 'HeartBtInt is negotiated once during Logon (35=A) and applies symmetrically.'},
        ]
    elif msg_type_val == 'A':
        return [
            {'color': 'blue',   'text': 'Logon (35=A) must be the first message on any new FIX session — no exceptions.'},
            {'color': 'green',  'text': 'Both counterparties must exchange Logon messages before trading messages can flow.'},
            {'color': 'orange', 'text': 'ResetSeqNumFlag=Y (141) resets both sides to sequence number 1 simultaneously.'},
            {'color': 'purple', 'text': 'HeartBtInt (108) sets the session heartbeat cadence in seconds.'},
        ]
    elif msg_type_val == '5':
        return [
            {'color': 'blue',   'text': 'Logout (35=5) gracefully terminates a FIX session.'},
            {'color': 'green',  'text': 'The receiving side must respond with their own Logout before closing the socket.'},
            {'color': 'orange', 'text': 'An unacknowledged Logout after timeout may result in a hard socket close.'},
            {'color': 'purple', 'text': 'Text (58) may optionally describe the reason for the logout.'},
        ]
    elif msg_type_val == 'F':
        return [
            {'color': 'blue',   'text': 'OrigClOrdID (41) links this cancel request to the original order.'},
            {'color': 'green',  'text': 'A new ClOrdID (11) is required — never reuse the OrigClOrdID value.'},
            {'color': 'orange', 'text': 'If rejected, an Order Cancel Reject (35=9) is returned by the broker.'},
            {'color': 'purple', 'text': 'Orders that are already fully filled or expired cannot be cancelled.'},
        ]
    elif msg_type_val == 'G':
        return [
            {'color': 'blue',   'text': 'Cancel/Replace (35=G) amends an existing order in one atomic operation.'},
            {'color': 'green',  'text': 'Any fills on the original order count toward the new order\'s CumQty.'},
            {'color': 'orange', 'text': 'New ClOrdID (11) required; OrigClOrdID (41) references the order being replaced.'},
            {'color': 'purple', 'text': 'If the replace fails, an Order Cancel Reject (35=9) is returned with the reason.'},
        ]
    elif msg_type_val == '3':
        return [
            {'color': 'blue',   'text': 'Session Reject (35=3) rejects a message at session level — not application level.'},
            {'color': 'orange', 'text': 'After receiving a reject, do NOT resend the same message unchanged.'},
            {'color': 'purple', 'text': 'SessionRejectReason (373) specifies exactly why the message was rejected.'},
            {'color': 'green',  'text': 'RefTagID (371) identifies the specific field that caused the rejection, if applicable.'},
        ]
    elif msg_type_val == '9':
        return [
            {'color': 'blue',   'text': 'Order Cancel Reject (35=9) is returned when a cancel or replace request fails.'},
            {'color': 'orange', 'text': 'The original order remains active — the cancel/replace did not take effect.'},
            {'color': 'purple', 'text': 'OrdStatus (39) reflects the current state of the original (unchanged) order.'},
        ]
    else:
        return [
            {'color': 'blue',   'text': 'MsgType (35) is always the second tag in any FIX message, right after BeginString (8).'},
            {'color': 'green',  'text': 'SenderCompID (49) and TargetCompID (56) form the session routing pair.'},
            {'color': 'orange', 'text': 'MsgSeqNum (34) increments by 1 for every message sent within a session.'},
            {'color': 'purple', 'text': 'CheckSum (10) is always the final tag in any FIX message.'},
        ]
