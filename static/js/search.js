/* ── FIXReader Search ─────────────────────────────────────────── */

(function() {
const SEARCH_INDEX = [

  /* MESSAGES */
  { type:'message', title:'Execution Report', subtitle:'MsgType (35) = 8', url:'/message-library', tag:'35', value:'8', aliases:['35=8','msgtype=8','execution report','exec report','er','execution','8'], related:['ordstatus','exectype','fill','partial fill','reject','ack','150','39'] },
  { type:'message', title:'New Order Single', subtitle:'MsgType (35) = D', url:'/message-library', tag:'35', value:'D', aliases:['35=d','msgtype=d','new order single','newordersingle','nos','d'], related:['clordid','ordtype','side','symbol','price','orderqty'] },
  { type:'message', title:'Order Cancel Request', subtitle:'MsgType (35) = F', url:'/message-library', tag:'35', value:'F', aliases:['35=f','cancel request','order cancel','cancel','f'], related:['origclordid','clordid'] },
  { type:'message', title:'Order Cancel/Replace Request', subtitle:'MsgType (35) = G', url:'/message-library', tag:'35', value:'G', aliases:['35=g','cancel replace','replace request','ocr','g'], related:['origclordid','price','orderqty'] },
  { type:'message', title:'Execution Report — Filled', subtitle:'OrdStatus (39) = 2', url:'/message-library', tag:'39', value:'2', aliases:['39=2','ordstatus=2','filled','full fill','fill'], related:['cumqty','leavesqty','avgpx'] },
  { type:'message', title:'Execution Report — Partial Fill', subtitle:'OrdStatus (39) = 1', url:'/message-library', tag:'39', value:'1', aliases:['39=1','ordstatus=1','partial fill','partial','partially filled'], related:['lastqty','cumqty','leavesqty'] },
  { type:'message', title:'Execution Report — New', subtitle:'OrdStatus (39) = 0', url:'/message-library', tag:'39', value:'0', aliases:['39=0','ordstatus=0','new ack','acknowledgement','ack','new order ack'], related:['clordid','orderid'] },
  { type:'message', title:'Execution Report — Canceled', subtitle:'OrdStatus (39) = 4', url:'/message-library', tag:'39', value:'4', aliases:['39=4','ordstatus=4','canceled','cancelled','cancel ack'], related:['origclordid'] },
  { type:'message', title:'Execution Report — Rejected', subtitle:'OrdStatus (39) = 8', url:'/message-library', tag:'39', value:'8', aliases:['39=8','ordstatus=8','rejected','reject','order reject'], related:['text','tag58'] },
  { type:'message', title:'Order Cancel Reject', subtitle:'MsgType (35) = 9', url:'/message-library', tag:'35', value:'9', aliases:['35=9','msgtype=9','cancel reject','cxl reject','9'], related:['cxlrejreason','origclordid'] },
  { type:'message', title:'Logon', subtitle:'MsgType (35) = A', url:'/message-library', tag:'35', value:'A', aliases:['35=a','msgtype=a','logon','login','session logon','a'], related:['heartbtint','resetseqnumflag','encryptmethod'] },
  { type:'message', title:'Logout', subtitle:'MsgType (35) = 5', url:'/message-library', tag:'35', value:'5', aliases:['35=5','msgtype=5','logout','session logout','5'], related:[] },
  { type:'message', title:'Heartbeat', subtitle:'MsgType (35) = 0', url:'/message-library', tag:'35', value:'0', aliases:['35=0','msgtype=0','heartbeat','hb','0'], related:['testreqid'] },
  { type:'message', title:'Test Request', subtitle:'MsgType (35) = 1', url:'/message-library', tag:'35', value:'1', aliases:['35=1','msgtype=1','test request','testrequest','1'], related:['testreqid'] },
  { type:'message', title:'Resend Request', subtitle:'MsgType (35) = 2', url:'/message-library', tag:'35', value:'2', aliases:['35=2','msgtype=2','resend request','resend','gap fill request','2'], related:['beginseqno','endseqno'] },
  { type:'message', title:'Reject', subtitle:'MsgType (35) = 3', url:'/message-library', tag:'35', value:'3', aliases:['35=3','msgtype=3','session reject','reject','3'], related:['refseqnum','reftagid','sessionrejectreason'] },
  { type:'message', title:'Sequence Reset', subtitle:'MsgType (35) = 4', url:'/message-library', tag:'35', value:'4', aliases:['35=4','msgtype=4','sequence reset','gap fill','gapfill','4'], related:['newseqno','gapfillflag'] },
  { type:'message', title:'Allocation Instruction', subtitle:'MsgType (35) = J', url:'/message-library', tag:'35', value:'J', aliases:['35=j','msgtype=j','allocation','alloc','allocation instruction','j'], related:['allocid','alloctranstype','noallocs','allocaccount'] },
  { type:'message', title:'Business Message Reject', subtitle:'MsgType (35) = j', url:'/message-library', tag:'35', value:'j', aliases:['35=j','msgtype=j','business reject','business message reject','bmr','j'], related:['refmsgtype','businessrejectreason'] },

  /* NEW MESSAGES */
  { type:'message', title:'Indication of Interest', subtitle:'MsgType (35) = 6', url:'/message-library', tag:'35', value:'6', aliases:['35=6','msgtype=6','msgtype 6','indication of interest','indicationofinterest','ioi','iois','indication','interest message'], related:['ioiqty','ioiqualifier','ioinaturalflag','ioitranstype','symbol','side'] },
  { type:'message', title:'Advertisement', subtitle:'MsgType (35) = 7', url:'/message-library', tag:'35', value:'7', aliases:['35=7','msgtype=7','advertisement','advert','7'], related:['advtranstype','advside','symbol'] },
  { type:'message', title:'Order Status Request', subtitle:'MsgType (35) = H', url:'/message-library', tag:'35', value:'H', aliases:['35=h','msgtype=h','order status request','order status','h'], related:['clordid','orderid'] },
  { type:'message', title:'Allocation Instruction Ack', subtitle:'MsgType (35) = P', url:'/message-library', tag:'35', value:'P', aliases:['35=p','msgtype=p','allocation ack','alloc ack','allocation acknowledgement','p'], related:['allocid','allocstatus','allocrejcode'] },
  { type:'message', title:"Don't Know Trade", subtitle:'MsgType (35) = Q', url:'/message-library', tag:'35', value:'Q', aliases:['35=q','msgtype=q','dont know trade','dk','dk trade','q'], related:['dkreason','execid'] },
  { type:'message', title:'New Order List', subtitle:'MsgType (35) = E', url:'/message-library', tag:'35', value:'E', aliases:['35=e','msgtype=e','new order list','order list','basket','e'], related:['listid','totnoorders'] },
  { type:'message', title:'List Cancel Request', subtitle:'MsgType (35) = K', url:'/message-library', tag:'35', value:'K', aliases:['35=k','msgtype=k','list cancel','list cancel request','k'], related:['listid'] },
  { type:'message', title:'List Execute', subtitle:'MsgType (35) = L', url:'/message-library', tag:'35', value:'L', aliases:['35=l','msgtype=l','list execute','l'], related:['listid'] },
  { type:'message', title:'List Status Request', subtitle:'MsgType (35) = M', url:'/message-library', tag:'35', value:'M', aliases:['35=m','msgtype=m','list status request','m'], related:['listid'] },
  { type:'message', title:'List Status', subtitle:'MsgType (35) = N', url:'/message-library', tag:'35', value:'N', aliases:['35=n','msgtype=n','list status','n'], related:['listid','listorderstatustype'] },
  { type:'message', title:'Market Data Request', subtitle:'MsgType (35) = V', url:'/message-library', tag:'35', value:'V', aliases:['35=v','msgtype=v','market data request','market data','v'], related:['mdreqid','subscriptionrequesttype'] },
  { type:'message', title:'Market Data Snapshot', subtitle:'MsgType (35) = W', url:'/message-library', tag:'35', value:'W', aliases:['35=w','msgtype=w','market data snapshot','snapshot','w'], related:['mdreqid','nomdentries'] },
  { type:'message', title:'Market Data Incremental Refresh', subtitle:'MsgType (35) = X', url:'/message-library', tag:'35', value:'X', aliases:['35=x','msgtype=x','market data incremental','incremental refresh','x'], related:['mdreqid'] },
  { type:'message', title:'Market Data Request Reject', subtitle:'MsgType (35) = Y', url:'/message-library', tag:'35', value:'Y', aliases:['35=y','msgtype=y','market data reject','md reject','y'], related:['mdreqid','mdreqrejreason'] },
  { type:'message', title:'Quote Request', subtitle:'MsgType (35) = R', url:'/message-library', tag:'35', value:'R', aliases:['35=r','msgtype=r','quote request','r'], related:['quoteReqid','symbol'] },
  { type:'message', title:'Quote', subtitle:'MsgType (35) = S', url:'/message-library', tag:'35', value:'S', aliases:['35=s','msgtype=s','quote','s'], related:['quoteid','bidpx','offerpx'] },
  { type:'message', title:'Settlement Instructions', subtitle:'MsgType (35) = T', url:'/message-library', tag:'35', value:'T', aliases:['35=t','msgtype=t','settlement instructions','settlement','t'], related:['settlinstid'] },
  { type:'message', title:'Security Definition', subtitle:'MsgType (35) = d', url:'/message-library', tag:'35', value:'d', aliases:['35=d-lower','msgtype=d-lower','security definition','secdef'], related:['symbol','securitytype'] },
  { type:'message', title:'Security Status', subtitle:'MsgType (35) = f', url:'/message-library', tag:'35', value:'f', aliases:['35=f-lower','msgtype=f-lower','security status'], related:['symbol','securitytradingstatus'] },
  { type:'message', title:'Trading Session Status', subtitle:'MsgType (35) = h', url:'/message-library', tag:'35', value:'h', aliases:['35=h-lower','msgtype=h-lower','trading session status','session status'], related:['tradingsessionid'] },
  { type:'message', title:'Mass Quote', subtitle:'MsgType (35) = i', url:'/message-library', tag:'35', value:'i', aliases:['35=i','msgtype=i','mass quote','i'], related:['quoteid','noquotesets'] },
  { type:'message', title:'Order Mass Cancel Request', subtitle:'MsgType (35) = q', url:'/message-library', tag:'35', value:'q', aliases:['35=q-lower','msgtype=q-lower','mass cancel','mass cancel request'], related:['masscancelrequesttype','symbol'] },
  { type:'message', title:'Order Mass Cancel Report', subtitle:'MsgType (35) = r', url:'/message-library', tag:'35', value:'r', aliases:['35=r-lower','msgtype=r-lower','mass cancel report'], related:['masscancelresponse'] },
  { type:'message', title:'New Order Cross', subtitle:'MsgType (35) = s', url:'/message-library', tag:'35', value:'s', aliases:['35=s-lower','msgtype=s-lower','new order cross','cross order'], related:['crosstype','crossid'] },

  /* TAGS */
  { type:'tag', title:'Tag 35 — MsgType', subtitle:'Message type identifier', url:'/tag/35', tag:'35', field:'MsgType', aliases:['35','tag 35','msgtype','message type'], related:[] },
  { type:'tag', title:'Tag 49 — SenderCompID', subtitle:'Identifies the firm sending the message', url:'/tag/49', tag:'49', field:'SenderCompID', aliases:['49','tag 49','sendercompid','sender','compid'], related:[] },
  { type:'tag', title:'Tag 56 — TargetCompID', subtitle:'Identifies the firm receiving the message', url:'/tag/56', tag:'56', field:'TargetCompID', aliases:['56','tag 56','targetcompid','target'], related:[] },
  { type:'tag', title:'Tag 55 — Symbol', subtitle:'Ticker symbol', url:'/tag/55', tag:'55', field:'Symbol', aliases:['55','tag 55','symbol','ticker','55=aapl'], related:[] },
  { type:'tag', title:'Tag 54 — Side', subtitle:'Buy or Sell', url:'/tag/54', tag:'54', field:'Side', aliases:['54','tag 54','side','buy','sell'], related:[] },
  { type:'tag', title:'Tag 11 — ClOrdID', subtitle:'Client order identifier', url:'/tag/11', tag:'11', field:'ClOrdID', aliases:['11','tag 11','clordid','client order id','order id'], related:[] },
  { type:'tag', title:'Tag 38 — OrderQty', subtitle:'Order quantity', url:'/tag/38', tag:'38', field:'OrderQty', aliases:['38','tag 38','orderqty','quantity','shares'], related:[] },
  { type:'tag', title:'Tag 44 — Price', subtitle:'Limit price', url:'/tag/44', tag:'44', field:'Price', aliases:['44','tag 44','price','limit price'], related:[] },
  { type:'tag', title:'Tag 40 — OrdType', subtitle:'Order type', url:'/tag/40', tag:'40', field:'OrdType', aliases:['40','tag 40','ordtype','order type'], related:[] },
  { type:'tag', title:'Tag 39 — OrdStatus', subtitle:'Order status', url:'/tag/39', tag:'39', field:'OrdStatus', aliases:['39','tag 39','ordstatus','order status'], related:[] },
  { type:'tag', title:'Tag 150 — ExecType', subtitle:'Type of execution', url:'/tag/150', tag:'150', field:'ExecType', aliases:['150','tag 150','exectype','execution type'], related:[] },
  { type:'tag', title:'Tag 17 — ExecID', subtitle:'Unique execution identifier', url:'/tag/17', tag:'17', field:'ExecID', aliases:['17','tag 17','execid','execution id'], related:[] },
  { type:'tag', title:'Tag 32 — LastQty', subtitle:'Quantity of last fill', url:'/tag/32', tag:'32', field:'LastQty', aliases:['32','tag 32','lastqty','last quantity','fill qty'], related:[] },
  { type:'tag', title:'Tag 14 — CumQty', subtitle:'Cumulative filled quantity', url:'/tag/14', tag:'14', field:'CumQty', aliases:['14','tag 14','cumqty','cumulative quantity'], related:[] },
  { type:'tag', title:'Tag 151 — LeavesQty', subtitle:'Remaining unfilled quantity', url:'/tag/151', tag:'151', field:'LeavesQty', aliases:['151','tag 151','leavesqty','leaves','remaining'], related:[] },
  { type:'tag', title:'Tag 8 — BeginString', subtitle:'FIX protocol version', url:'/tag/8', tag:'8', field:'BeginString', aliases:['8','tag 8','beginstring','fix version'], related:[] },
  { type:'tag', title:'Tag 10 — CheckSum', subtitle:'Message checksum', url:'/tag/10', tag:'10', field:'CheckSum', aliases:['10','tag 10','checksum','check sum'], related:[] },
  { type:'tag', title:'Tag 52 — SendingTime', subtitle:'Time message was sent', url:'/tag/52', tag:'52', field:'SendingTime', aliases:['52','tag 52','sendingtime','sending time','timestamp'], related:[] },
  { type:'tag', title:'Tag 59 — TimeInForce', subtitle:'Order time in force', url:'/tag/59', tag:'59', field:'TimeInForce', aliases:['59','tag 59','timeinforce','tif'], related:[] },
  { type:'tag', title:'Tag 41 — OrigClOrdID', subtitle:'Original client order ID for cancel/replace', url:'/tag/41', tag:'41', field:'OrigClOrdID', aliases:['41','tag 41','origclordid','original order id'], related:[] },
  { type:'tag', title:'Tag 43 — PossDup', subtitle:'Possible duplicate flag', url:'/tag/43', tag:'43', field:'PossDup', aliases:['43','tag 43','possdupflag','posdup','possible duplicate','duplicate resend','43=y'], related:[] },
  { type:'tag', title:'Tag 34 — MsgSeqNum', subtitle:'Message sequence number', url:'/tag/34', tag:'34', field:'MsgSeqNum', aliases:['34','tag 34','msgseqnum','sequence number','seq num'], related:[] },
  { type:'tag', title:'Tag 108 — HeartBtInt', subtitle:'Heartbeat interval in seconds', url:'/tag/108', tag:'108', field:'HeartBtInt', aliases:['108','tag 108','heartbtint','heartbeat interval'], related:[] },
  { type:'tag', title:'Tag 141 — ResetSeqNumFlag', subtitle:'Reset sequence numbers on logon', url:'/tag/141', tag:'141', field:'ResetSeqNumFlag', aliases:['141','tag 141','resetseqnumflag','reset seq','141=y'], related:[] },

  /* ENUM VALUES */
  { type:'enum', title:'Side = Buy', subtitle:'Tag 54 = 1', url:'/tag/54', tag:'54', field:'Side', value:'1', aliases:['54=1','side=1','buy','side buy'], description:'Buy order' },
  { type:'enum', title:'Side = Sell', subtitle:'Tag 54 = 2', url:'/tag/54', tag:'54', field:'Side', value:'2', aliases:['54=2','side=2','sell','side sell'], description:'Sell order' },
  { type:'enum', title:'TimeInForce = IOC', subtitle:'Tag 59 = 3', url:'/tag/59', tag:'59', field:'TimeInForce', value:'3', aliases:['59=3','ioc','immediate or cancel','timeinforce ioc','timeinforce 3'], description:'Immediate or Cancel' },
  { type:'enum', title:'TimeInForce = FOK', subtitle:'Tag 59 = 4', url:'/tag/59', tag:'59', field:'TimeInForce', value:'4', aliases:['59=4','fok','fill or kill','timeinforce fok','timeinforce 4'], description:'Fill or Kill' },
  { type:'enum', title:'TimeInForce = Day', subtitle:'Tag 59 = 0', url:'/tag/59', tag:'59', field:'TimeInForce', value:'0', aliases:['59=0','day','day order','timeinforce day'], description:'Day order' },
  { type:'enum', title:'TimeInForce = GTC', subtitle:'Tag 59 = 1', url:'/tag/59', tag:'59', field:'TimeInForce', value:'1', aliases:['59=1','gtc','good till cancel','timeinforce gtc'], description:'Good Till Cancel' },
  { type:'enum', title:'OrdType = Market', subtitle:'Tag 40 = 1', url:'/tag/40', tag:'40', field:'OrdType', value:'1', aliases:['40=1','ordtype=1','market order','market'], description:'Market order' },
  { type:'enum', title:'OrdType = Limit', subtitle:'Tag 40 = 2', url:'/tag/40', tag:'40', field:'OrdType', value:'2', aliases:['40=2','ordtype=2','limit order','limit'], description:'Limit order' },
  { type:'enum', title:'ExecType = Trade', subtitle:'Tag 150 = F', url:'/tag/150', tag:'150', field:'ExecType', value:'F', aliases:['150=f','exectype=f','trade','fill','exectype trade'], description:'Trade (fill)' },
  { type:'enum', title:'ExecType = New', subtitle:'Tag 150 = 0', url:'/tag/150', tag:'150', field:'ExecType', value:'0', aliases:['150=0','exectype=0','new ack','exectype new'], description:'New acknowledgement' },
  { type:'enum', title:'ExecType = Canceled', subtitle:'Tag 150 = 4', url:'/tag/150', tag:'150', field:'ExecType', value:'4', aliases:['150=4','exectype=4','canceled','exectype canceled'], description:'Canceled' },
  { type:'enum', title:'ExecType = Rejected', subtitle:'Tag 150 = 8', url:'/tag/150', tag:'150', field:'ExecType', value:'8', aliases:['150=8','exectype=8','rejected','exectype rejected'], description:'Rejected' },
  { type:'enum', title:'PossDup = Y', subtitle:'Tag 43 = Y', url:'/tag/43', tag:'43', field:'PossDup', value:'Y', aliases:['43=y','possdupflag=y','possible duplicate','duplicate message','posdup'], description:'Possible duplicate' },
  { type:'enum', title:'GapFillFlag = Y', subtitle:'Tag 123 = Y', url:'/tag/123', tag:'123', field:'GapFillFlag', value:'Y', aliases:['123=y','gapfillflag=y','gap fill','gapfill'], description:'Gap fill' },
  { type:'enum', title:'ResetSeqNumFlag = Y', subtitle:'Tag 141 = Y', url:'/tag/141', tag:'141', field:'ResetSeqNumFlag', value:'Y', aliases:['141=y','resetseqnumflag=y','reset sequence','reset seq num'], description:'Reset sequence numbers' },

  /* EXCHANGES */
  { type:'exchange', title:'NYSE Order Entry', subtitle:'Exchange Spec · XNYS', url:'/exchange-specs', exchange:'NYSE', aliases:['nyse session','nyse order entry','nyse order session','nyse trading session','nyse fix','xnys'] },
  { type:'exchange', title:'NYSE Drop Copy', subtitle:'Exchange Spec · XNYS', url:'/exchange-specs', exchange:'NYSE', aliases:['nyse drop copy','nyse dropcopy','nyse execution feed'] },
  { type:'exchange', title:'NASDAQ', subtitle:'Exchange Spec · XNAS', url:'/exchange-specs', exchange:'NASDAQ', aliases:['nasdaq','xnas','nasdaq route','nasdaq order entry','nasdaq fix'] },
  { type:'exchange', title:'NYSE Arca', subtitle:'Exchange Spec · ARCX', url:'/exchange-specs', exchange:'NYSE Arca', aliases:['arca','arcx','nyse arca','arca destination','arca route'] },
  { type:'exchange', title:'CBOE BZX', subtitle:'Exchange Spec · XCBO', url:'/exchange-specs', exchange:'CBOE', aliases:['cboe','cboe bzx','xcbo','cboe session','cboe fix'] },
  { type:'exchange', title:'EDGX', subtitle:'Exchange Spec · EDGX', url:'/exchange-specs', exchange:'EDGX', aliases:['edgx','edgx routing','edgx fix','edgx session'] },
  { type:'exchange', title:'EDGA', subtitle:'Exchange Spec · EDGA', url:'/exchange-specs', exchange:'EDGA', aliases:['edga','edga routing','edga fix'] },
  { type:'exchange', title:'IEX', subtitle:'Exchange Spec · IEXG', url:'/exchange-specs', exchange:'IEX', aliases:['iex','iexg','iex session','iex fix','investors exchange'] },

  /* TOOLS */
  { type:'tool', title:'FIX Decoder', subtitle:'Decode and analyze FIX messages', url:'/', aliases:['decoder','fix decoder','decode','parse fix'] },
  { type:'tool', title:'Compare Messages', subtitle:'Diff two FIX messages', url:'/compare', aliases:['compare','diff','message diff','fix diff'] },
  { type:'tool', title:'Message Builder', subtitle:'Build valid FIX messages', url:'/tools/message-builder', aliases:['builder','message builder','build fix','fix builder'] },
  { type:'tool', title:'Tag Validator', subtitle:'Validate FIX tag combinations', url:'/tools/tag-validator', aliases:['validator','tag validator','validate','fix validate'] },

  /* CERTIFICATION */
  { type:'cert', title:'Order Entry Certification', subtitle:'Cert Scripts', url:'/cert/order-entry', aliases:['order entry cert','order entry certification','oe cert','certification'] },
  { type:'cert', title:'Drop Copy Certification', subtitle:'Cert Scripts', url:'/cert/drop-copy', aliases:['drop copy cert','drop copy certification','dc cert'] },
  { type:'cert', title:'Allocation Certification', subtitle:'Cert Scripts', url:'/cert/allocation', aliases:['allocation cert','allocation certification','alloc cert'] },
  { type:'cert', title:'IOC Certification Test', subtitle:'Order Entry · Phase 3', url:'/cert/order-entry', aliases:['ioc cert','ioc test','immediate or cancel cert'] },
  { type:'cert', title:'Gap Fill Recovery', subtitle:'Order Entry · Phase 6', url:'/cert/order-entry', aliases:['gap fill cert','gap fill recovery','gap fill test'] },
  { type:'cert', title:'Duplicate ClOrdID', subtitle:'Reject Scenarios · Phase 6', url:'/cert/order-entry', aliases:['duplicate clordid','duplicate order id','clordid duplicate'] },
  { type:'cert', title:'PossDup Processing', subtitle:'Advanced · Phase 6', url:'/cert/order-entry', aliases:['possdupflag cert','posdup test','possible duplicate cert'] },

  /* TROUBLESHOOTING */
  { type:'troubleshooting', title:'Network & Connectivity', subtitle:'Troubleshooting', url:'/troubleshooting/network', aliases:['network','connectivity','tcp','connection','firewall'] },
  { type:'troubleshooting', title:'Sequence Number Issues', subtitle:'Troubleshooting', url:'/troubleshooting/sequence-numbers', aliases:['sequence numbers','seq num','msgseqnum','out of sequence','gap','resend'] },
  { type:'troubleshooting', title:'Logon Failures', subtitle:'Troubleshooting', url:'/troubleshooting/logon', aliases:['logon failure','login failure','logon reject','session reject logon'] },
  { type:'troubleshooting', title:'Fill Reconciliation', subtitle:'Troubleshooting', url:'/troubleshooting/fill-reconciliation', aliases:['fill reconciliation','fill recon','cumqty mismatch','lastqty','missing fill'] },
  { type:'troubleshooting', title:'Order Rejects', subtitle:'Troubleshooting', url:'/troubleshooting/rejects', aliases:['order rejects','rejected order','reject','execution report reject','ordstatus 8','150=8','39=8','35=3','35=j','35=9','371','373','duplicate clordid','invalid account','invalid symbol','risk reject','session reject','ord rej reason','ordrejmreason','business message reject','bmr'] },
  { type:'troubleshooting', title:'Duplicate Orders', subtitle:'Troubleshooting', url:'/troubleshooting/duplicate-orders', aliases:['duplicate orders','duplicate clordid','duplicate order','resend order'] },
  { type:'troubleshooting', title:'Gap Fill & Resend', subtitle:'Troubleshooting', url:'/troubleshooting/gap-fill', aliases:['gap fill','resend request','sequence gap','missing messages'] },
];

const FIXREADER_TAG_ENUM = {
  1: { name: 'Account', desc: 'Account mnemonic for clearing and allocation' },
  6: { name: 'AvgPx', desc: 'Calculated average price of fills' },
  7: { name: 'BeginSeqNo', desc: 'Beginning sequence number for resend range' },
  8: { name: 'BeginString', desc: 'FIX protocol version identifier' },
  9: { name: 'BodyLength', desc: 'Message length in bytes' },
  10: { name: 'CheckSum', desc: 'Three-digit modulo-256 checksum' },
  11: { name: 'ClOrdID', desc: 'Unique client order identifier' },
  12: { name: 'Commission', desc: 'Commission amount for order or fill' },
  13: { name: 'CommType', desc: 'Commission type indicator' },
  14: { name: 'CumQty', desc: 'Total filled quantity to date' },
  15: { name: 'Currency', desc: 'ISO 4217 currency code for order denomination' },
  16: { name: 'EndSeqNo', desc: 'Ending sequence number for resend range' },
  17: { name: 'ExecID', desc: 'Unique execution identifier' },
  18: { name: 'ExecInst', desc: 'Order handling instructions — multiple values space-separated', values: { '0':'Stay on offer side','1':'Not held — trader has discretion','2':'Work — work with discretion','3':'Go along — participate alongside market','4':'Over the day','5':'Held — execute immediately','6':"Participate, don't initiate",'7':'Strict scale','8':'Try to scale','9':'Stay on bid side','A':'No cross','B':'OK to cross','C':'Call first','D':'Percent of volume','E':'Do not increase (DNI)','F':'Do not reduce (DNR)','G':'All or none (AON)','I':'Reinstate on system failure','J':'Institutions only','K':'Reinstate on trading halt','L':'Cancel on trading halt','M':'Last peg','N':'Mid-price peg','O':'Non-negotiable','P':'Opening peg','Q':'Market peg','R':'Cancel on system failure','S':'Primary peg','T':'Suspend','X':'Peg to VWAP' } },
  20: { name: 'ExecTransType', desc: 'Execution transaction type' },
  21: { name: 'HandlInst', desc: 'Order handling instructions for broker', values: { '1':'Automated execution — no broker intervention','2':'Automated execution — broker OK','3':'Manual order — best execution' } },
  22: { name: 'SecurityIDSource', desc: 'Source of SecurityID value', values: { '1':'CUSIP','2':'SEDOL','3':'QUIK','4':'ISIN','5':'RIC code','6':'ISO Currency Code','7':'ISO Country Code','8':'Exchange Symbol','9':'CTA Symbol','A':'Bloomberg Symbol','B':'Wertpapier','C':'Dutch','D':'Valoren','E':'Sicovam','F':'Belgian','G':'Common (Clearstream and Euroclear)' } },
  30: { name: 'LastMkt', desc: 'Market where last execution occurred' },
  31: { name: 'LastPx', desc: 'Price of last fill' },
  32: { name: 'LastQty', desc: 'Quantity of last fill' },
  34: { name: 'MsgSeqNum', desc: 'Message sequence number' },
  35: { name: 'MsgType', desc: 'Identifies message type', values: { '0':'Heartbeat','1':'Test Request','2':'Resend Request','3':'Reject','4':'Sequence Reset','5':'Logout','6':'IOI','7':'Advertisement','8':'Execution Report','9':'Order Cancel Reject','A':'Logon','B':'News','C':'Email','D':'New Order Single','E':'New Order List','F':'Order Cancel Request','G':'Order Cancel/Replace Request','H':'Order Status Request','J':'Allocation Instruction','P':'Allocation Instruction Ack','Q':"Don't Know Trade",'R':'Quote Request','S':'Quote','T':'Settlement Instructions','V':'Market Data Request','W':'Market Data Snapshot','X':'Market Data Incremental Refresh','Y':'Market Data Request Reject','Z':'Quote Cancel','i':'Mass Quote','j':'Business Message Reject','q':'Order Mass Cancel Request','r':'Order Mass Cancel Report','s':'New Order Cross','AE':'Trade Capture Report','AS':'Allocation Report' } },
  36: { name: 'NewSeqNo', desc: 'New sequence number after reset' },
  37: { name: 'OrderID', desc: 'Exchange assigned order identifier' },
  38: { name: 'OrderQty', desc: 'Number of shares or contracts ordered' },
  39: { name: 'OrdStatus', desc: 'Current order status', values: { '0':'New','1':'Partially Filled','2':'Filled','3':'Done For Day','4':'Canceled','5':'Replaced','6':'Pending Cancel','7':'Stopped','8':'Rejected','9':'Suspended','A':'Pending New','B':'Calculated','C':'Expired','D':'Accepted For Bidding','E':'Pending Replace' } },
  40: { name: 'OrdType', desc: 'Order type', values: { '1':'Market','2':'Limit','3':'Stop','4':'Stop Limit','5':'Market On Close','7':'Market To Limit','P':'Pegged' } },
  41: { name: 'OrigClOrdID', desc: 'Original client order ID for cancel or replace' },
  43: { name: 'PossDupFlag', desc: 'Possible duplicate flag', values: { 'Y':'Yes — possible duplicate','N':'No — not a duplicate' } },
  44: { name: 'Price', desc: 'Limit price per unit of quantity' },
  45: { name: 'RefSeqNum', desc: 'Reference sequence number for reject' },
  47: { name: 'Rule80A', desc: 'Order capacity under NYSE Rule 80A' },
  48: { name: 'SecurityID', desc: 'Security identifier value' },
  49: { name: 'SenderCompID', desc: 'Identifies firm sending the message' },
  50: { name: 'SenderSubID', desc: 'Sub-identifier for message originator' },
  52: { name: 'SendingTime', desc: 'UTC time message was transmitted' },
  53: { name: 'Shares', desc: 'Number of shares' },
  54: { name: 'Side', desc: 'Side of order', values: { '1':'Buy','2':'Sell','3':'Buy Minus','4':'Sell Plus','5':'Sell Short','6':'Sell Short Exempt','7':'Undisclosed','8':'Cross (as dealer)','9':'Cross Short' } },
  55: { name: 'Symbol', desc: 'Ticker symbol' },
  56: { name: 'TargetCompID', desc: 'Identifies firm receiving the message' },
  57: { name: 'TargetSubID', desc: 'Sub-identifier for message recipient' },
  58: { name: 'Text', desc: 'Free format text string' },
  59: { name: 'TimeInForce', desc: 'How long order remains active', values: { '0':'Day','1':'GTC — Good Till Cancel','2':'At the Opening','3':'IOC — Immediate or Cancel','4':'FOK — Fill or Kill','5':'Good Till Crossing (GTX)','6':'GTD — Good Till Date','7':'At the Close' } },
  60: { name: 'TransactTime', desc: 'UTC time of transaction' },
  63: { name: 'SettlType', desc: 'Indicates order settlement period' },
  64: { name: 'SettlDate', desc: 'Specific date of trade settlement' },
  65: { name: 'SymbolSfx', desc: 'Additional information about symbol' },
  66: { name: 'ListID', desc: 'Identifier for a list order' },
  70: { name: 'AllocID', desc: 'Unique identifier for allocation message' },
  71: { name: 'AllocTransType', desc: 'Allocation transaction type', values: { '0':'New','1':'Replace','2':'Cancel','3':'Preliminary','4':'Calculated','5':'Calculated Without Preliminary' } },
  73: { name: 'NoOrders', desc: 'Number of orders in allocation' },
  75: { name: 'TradeDate', desc: 'Indicates date of trade referenced' },
  76: { name: 'ExecBroker', desc: 'Executing broker identifier' },
  78: { name: 'NoAllocs', desc: 'Number of allocation accounts' },
  79: { name: 'AllocAccount', desc: 'Sub-account for allocation' },
  80: { name: 'AllocShares', desc: 'Number of shares allocated to account' },
  87: { name: 'AllocStatus', desc: 'Status of allocation', values: { '0':'Accepted','1':'Rejected','2':'Partial Accept','3':'Received','4':'Incomplete','5':'Claim','6':'Disputed','7':'Processing Alert' } },
  88: { name: 'AllocRejCode', desc: 'Allocation rejection reason', values: { '0':'Unknown account','1':'Incorrect quantity','2':'Incorrect average price','3':'Unknown executing broker','4':'Commission difference','5':'Unknown OrderID','6':'Unknown ListID','7':'Other' } },
  97: { name: 'PossResend', desc: 'Indicates message may be retransmission' },
  98: { name: 'EncryptMethod', desc: 'Encryption method', values: { '0':'None — TLS handled at transport layer','1':'PKCS','2':'DES','3':'PKCS/DES','4':'PGP/DES','5':'PGP/DES-MD5','6':'PEM/DES-MD5' } },
  99: { name: 'StopPx', desc: 'Stop price for stop or stop limit order' },
  100: { name: 'ExDestination', desc: 'Exchange or market routing destination' },
  102: { name: 'CxlRejReason', desc: 'Cancel reject reason', values: { '0':'Too late to cancel','1':'Unknown order','2':'Broker/exchange option','3':'Order already pending','4':'Unable to process mass cancel','5':'OrigOrdModTime mismatch','6':'Duplicate ClOrdID' } },
  103: { name: 'OrdRejReason', desc: 'Order rejection reason', values: { '0':'Broker/exchange option','1':'Unknown symbol','2':'Exchange closed','3':'Order exceeds limit','4':'Too late to enter','5':'Unknown order','6':'Duplicate order','7':'Duplicate verbal order','8':'Stale order','9':'Trade along required','10':'Invalid investor ID','11':'Unsupported order characteristic','12':'Surveillance option','13':'Incorrect quantity','14':'Incorrect allocated quantity','15':'Unknown account','99':'Other' } },
  107: { name: 'SecurityDesc', desc: 'Security description' },
  108: { name: 'HeartBtInt', desc: 'Heartbeat interval in seconds' },
  109: { name: 'ClientID', desc: 'Unique identifier for client' },
  110: { name: 'MinQty', desc: 'Minimum quantity for execution' },
  111: { name: 'MaxFloor', desc: 'Maximum quantity to display on exchange book — iceberg/reserve quantity' },
  112: { name: 'TestReqID', desc: 'Identifier for test request — must be echoed in Heartbeat response' },
  113: { name: 'ReportToExch', desc: 'Indicates if reporting to exchange' },
  114: { name: 'LocateReqd', desc: 'Indicates if borrow locate is required for short sale' },
  115: { name: 'OnBehalfOfCompID', desc: 'Firm sending on behalf of another' },
  116: { name: 'OnBehalfOfSubID', desc: 'Sub-ID for on-behalf-of firm' },
  117: { name: 'QuoteID', desc: 'Unique identifier for quote' },
  120: { name: 'SettlCurrency', desc: 'Settlement currency for trade' },
  121: { name: 'ForexReq', desc: 'Indicates request for forex accommodation' },
  122: { name: 'OrigSendingTime', desc: 'Original sending time on retransmitted message' },
  123: { name: 'GapFillFlag', desc: 'Sequence reset is gap fill', values: { 'Y':'Yes — skip these sequence numbers','N':'No — hard reset to NewSeqNo' } },
  124: { name: 'NoExecs', desc: 'Number of executions' },
  126: { name: 'ExpireTime', desc: 'UTC time order expires' },
  128: { name: 'DeliverToCompID', desc: 'Target firm for delivery' },
  130: { name: 'IOINaturalFlag', desc: 'Indicates natural IOI' },
  131: { name: 'QuoteReqID', desc: 'Unique identifier for quote request' },
  132: { name: 'BidPx', desc: 'Bid price' },
  133: { name: 'OfferPx', desc: 'Offer price' },
  134: { name: 'BidSize', desc: 'Quantity of bid' },
  135: { name: 'OfferSize', desc: 'Quantity of offer' },
  136: { name: 'NoMiscFees', desc: 'Number of miscellaneous fees' },
  137: { name: 'MiscFeeAmt', desc: 'Miscellaneous fee amount' },
  138: { name: 'MiscFeeCurr', desc: 'Currency for miscellaneous fee' },
  139: { name: 'MiscFeeType', desc: 'Type of miscellaneous fee' },
  140: { name: 'PrevClosePx', desc: 'Previous closing price' },
  141: { name: 'ResetSeqNumFlag', desc: 'Reset sequence numbers on logon', values: { 'Y':'Yes — reset both sides to 1','N':'No — continue existing sequence numbers' } },
  142: { name: 'SenderLocationID', desc: 'Sender location identifier' },
  143: { name: 'TargetLocationID', desc: 'Target location identifier' },
  144: { name: 'OnBehalfOfLocationID', desc: 'On-behalf-of location identifier' },
  145: { name: 'DeliverToLocationID', desc: 'Deliver-to location identifier' },
  146: { name: 'NoRelatedSym', desc: 'Number of related symbols' },
  147: { name: 'Subject', desc: 'Subject of email' },
  148: { name: 'Headline', desc: 'Headline of news' },
  149: { name: 'URLLink', desc: 'URL link' },
  150: { name: 'ExecType', desc: 'Type of execution report', values: { '0':'New','1':'Partial Fill','2':'Fill','3':'Done For Day','4':'Canceled','5':'Replaced','6':'Pending Cancel','7':'Stopped','8':'Rejected','9':'Suspended','A':'Pending New','B':'Calculated','C':'Expired','D':'Restated','E':'Pending Replace','F':'Trade (partial fill or fill)','G':'Trade Correct','H':'Trade Cancel','I':'Order Status' } },
  151: { name: 'LeavesQty', desc: 'Quantity open for further execution' },
  152: { name: 'CashOrderQty', desc: 'Order quantity in cash' },
  153: { name: 'AllocAvgPx', desc: 'Average price for allocation' },
  154: { name: 'AllocNetMoney', desc: 'Net money for allocation' },
  155: { name: 'SettlCurrFxRate', desc: 'Foreign exchange rate for settlement currency' },
  156: { name: 'SettlCurrFxRateCalc', desc: 'Method for FX rate calculation' },
  157: { name: 'NumDaysInterest', desc: 'Number of days accrued interest' },
  158: { name: 'AccruedInterestRate', desc: 'Accrued interest rate' },
  159: { name: 'AccruedInterestAmt', desc: 'Accrued interest amount' },
  160: { name: 'SettlInstMode', desc: 'Settlement instruction mode' },
  161: { name: 'AllocText', desc: 'Free format text for allocation' },
  162: { name: 'SettlInstID', desc: 'Unique identifier for settlement instructions' },
  163: { name: 'SettlInstTransType', desc: 'Transaction type for settlement instructions' },
  164: { name: 'EmailThreadID', desc: 'Thread identifier for email' },
  165: { name: 'SettlInstSource', desc: 'Source of settlement instructions' },
  166: { name: 'SettlLocation', desc: 'Settlement location' },
  167: { name: 'SecurityType', desc: 'Indicates type of security' },
  168: { name: 'EffectiveTime', desc: 'Time order becomes effective' },
  169: { name: 'StandInstDbType', desc: 'Standing instruction database type' },
  170: { name: 'StandInstDbName', desc: 'Standing instruction database name' },
  171: { name: 'StandInstDbID', desc: 'Standing instruction database identifier' },
  172: { name: 'SettlDeliveryType', desc: 'Settlement delivery type' },
  173: { name: 'SettlDepositoryCode', desc: 'Settlement depository code' },
  174: { name: 'SettlBrkrCode', desc: 'Settlement broker code' },
  175: { name: 'SettlInstCode', desc: 'Settlement instruction code' },
  176: { name: 'SecuritySettlAgentName', desc: 'Security settlement agent name' },
  177: { name: 'SecuritySettlAgentCode', desc: 'Security settlement agent code' },
  178: { name: 'SecuritySettlAgentAcctNum', desc: 'Security settlement agent account number' },
  179: { name: 'SecuritySettlAgentAcctName', desc: 'Security settlement agent account name' },
  180: { name: 'SecuritySettlAgentContactName', desc: 'Security settlement agent contact name' },
  181: { name: 'SecuritySettlAgentContactPhone', desc: 'Security settlement agent contact phone' },
  182: { name: 'CashSettlAgentName', desc: 'Cash settlement agent name' },
  183: { name: 'CashSettlAgentCode', desc: 'Cash settlement agent code' },
  184: { name: 'CashSettlAgentAcctNum', desc: 'Cash settlement agent account number' },
  185: { name: 'CashSettlAgentAcctName', desc: 'Cash settlement agent account name' },
  186: { name: 'CashSettlAgentContactName', desc: 'Cash settlement agent contact name' },
  187: { name: 'CashSettlAgentContactPhone', desc: 'Cash settlement agent contact phone' },
  188: { name: 'BidSpotRate', desc: 'Bid spot rate for FX' },
  189: { name: 'BidForwardPoints', desc: 'Bid forward points for FX' },
  190: { name: 'OfferSpotRate', desc: 'Offer spot rate for FX' },
  191: { name: 'OfferForwardPoints', desc: 'Offer forward points for FX' },
  192: { name: 'OrderQty2', desc: 'Order quantity for leg 2 of FX swap' },
  193: { name: 'SettlDate2', desc: 'Settlement date for leg 2 of FX swap' },
  194: { name: 'LastSpotRate', desc: 'Last spot rate for FX' },
  195: { name: 'LastForwardPoints', desc: 'Last forward points for FX' },
  196: { name: 'AllocLinkID', desc: 'Allocation link identifier' },
  197: { name: 'AllocLinkType', desc: 'Allocation link type' },
  198: { name: 'SecondaryOrderID', desc: 'Secondary order identifier' },
  199: { name: 'NoIOIQualifiers', desc: 'Number of IOI qualifiers' },
  200: { name: 'MaturityMonthYear', desc: 'Month and year of maturity for futures' },
  201: { name: 'PutOrCall', desc: 'Put or call indicator', values: { '0':'Put','1':'Call' } },
  202: { name: 'StrikePrice', desc: 'Strike price for options' },
  203: { name: 'CoveredOrUncovered', desc: 'Covered or uncovered indicator' },
  204: { name: 'CustomerOrFirm', desc: 'Customer or firm indicator' },
  205: { name: 'MaturityDay', desc: 'Day of maturity for futures' },
  206: { name: 'OptAttribute', desc: 'Option attribute' },
  207: { name: 'SecurityExchange', desc: 'Market identifier code (MIC) — used with Tag 48 to identify exchange' },
  208: { name: 'NotifyBrokerOfCredit', desc: 'Notify broker of credit' },
  209: { name: 'AllocHandlInst', desc: 'Allocation handling instruction' },
  210: { name: 'MaxShow', desc: 'Maximum quantity shown on exchange book' },
  211: { name: 'PegOffsetValue', desc: 'IEX peg offset — used with D-Peg and P-Peg order types' },
  212: { name: 'XmlDataLen', desc: 'Length of XML data' },
  213: { name: 'XmlData', desc: 'XML data' },
  214: { name: 'SettlInstRefID', desc: 'Settlement instruction reference identifier' },
  215: { name: 'NoRoutingIDs', desc: 'Number of routing identifiers' },
  216: { name: 'RoutingType', desc: 'Type of routing identifier' },
  217: { name: 'RoutingID', desc: 'Routing identifier value' },
  291: { name: 'FinancialStatus', desc: 'Financial status of security' },
  292: { name: 'CorporateAction', desc: 'Corporate action type' },
  336: { name: 'TradingSessionID', desc: 'Trading session identifier — used by NYSE Pillar and others', values: { '1': 'Pre-Market / Early Trading Session', '2': 'Core Trading Session', '3': 'After Hours / Late Trading Session', '4': 'Early Core Session', '5': 'Core and Late Session', '6': 'Early Core and Late Session' } },
  371: { name: 'RefTagID', desc: 'Tag number referenced in reject message' },
  372: { name: 'RefMsgType', desc: 'Message type referenced in business reject' },
  373: { name: 'SessionRejectReason', desc: 'Session reject reason', values: { '0':'Invalid tag number','1':'Required tag missing','2':'Tag not defined for message type','3':'Undefined tag','4':'Tag specified without value','5':'Incorrect value for tag','6':'Incorrect data format','7':'Decryption problem','8':'Signature problem','9':'CompID problem','10':'SendingTime accuracy problem','11':'Invalid MsgType','99':'Other' } },
  374: { name: 'BidRequestTransType', desc: 'Bid request transaction type' },
  375: { name: 'ContraBroker', desc: 'Contra broker identifier' },
  376: { name: 'ComplianceID', desc: 'Compliance identifier' },
  377: { name: 'SolicitedFlag', desc: 'Indicates if order was solicited' },
  378: { name: 'ExecRestatementReason', desc: 'Reason for execution restatement' },
  379: { name: 'BusinessRejectRefID', desc: 'Reference identifier for business reject' },
  380: { name: 'BusinessRejectReason', desc: 'Business reject reason', values: { '0':'Other','1':'Unknown ID','2':'Unknown security','3':'Unsupported message type','4':'Application not available','5':'Conditionally required field missing','6':'Not authorized','7':'DeliverTo firm not available' } },
  381: { name: 'GrossTradeAmt', desc: 'Gross trade amount' },
  382: { name: 'NoContraBrokers', desc: 'Number of contra brokers' },
  383: { name: 'MaxMessageSize', desc: 'Maximum message size' },
  384: { name: 'NoMsgTypes', desc: 'Number of message types' },
  385: { name: 'MsgDirection', desc: 'Indicates if message type is send or receive' },
  386: { name: 'NoTradingSessions', desc: 'Number of trading sessions' },
  387: { name: 'TotalVolumeTraded', desc: 'Total volume traded' },
  388: { name: 'DiscretionInst', desc: 'Discretion instruction' },
  389: { name: 'DiscretionOffsetValue', desc: 'Discretion offset value' },
  390: { name: 'BidID', desc: 'Unique identifier for bid' },
  391: { name: 'ClientBidID', desc: 'Client bid identifier' },
  392: { name: 'ListName', desc: 'List name identifier' },
  393: { name: 'TotNoRelatedSym', desc: 'Total number of related symbols' },
  394: { name: 'BidType', desc: 'Type of bid' },
  395: { name: 'NumTickets', desc: 'Number of tickets' },
  396: { name: 'SideValue1', desc: 'Side value 1' },
  397: { name: 'SideValue2', desc: 'Side value 2' },
  432: { name: 'ExpireDate', desc: 'Date order expires' },
  434: { name: 'CxlRejResponseTo', desc: 'Cancel reject response to', values: { '1':'Order Cancel Request','2':'Order Cancel/Replace Request' } },
  439: { name: 'ClearingFirm', desc: 'Clearing firm identifier' },
  440: { name: 'ClearingAccount', desc: 'Clearing account identifier' },
  448: { name: 'PartyID', desc: 'Party identifier' },
  452: { name: 'PartyRole', desc: 'Identifies role of PartyID' },
  453: { name: 'NoPartyIDs', desc: 'Number of party identifiers' },
  461: { name: 'CFICode', desc: 'ISO 10962 Classification of Financial Instruments code' },
  470: { name: 'CountryOfIssue', desc: 'ISO 3166 country code of issuance' },
  553: { name: 'Username', desc: 'Username for logon authentication' },
  554: { name: 'Password', desc: 'Password for logon authentication' },
  /* ── Exchange-specific tags ── */
  1409: { name: 'SessionStatus', desc: 'Session status on logout', values: { '0': 'Session active', '1': 'Session password changed', '2': 'Session password due to expire', '3': 'New session password does not comply', '4': 'Session logout complete', '5': 'Invalid username or password', '6': 'Account locked', '7': 'Logons not allowed at this time', '100': 'Other' } },
  7928: { name: 'SelfTradeType', desc: 'NYSE self-trade prevention type', values: { 'T': 'No STP', 'N': 'Cancel Newest', 'O': 'Cancel Oldest', 'C': 'Cancel Both', 'D': 'Decrement' } },
  9000: { name: 'OrderInstructions', desc: 'NASDAQ order instructions byte' },
  9200: { name: 'PostOnly', desc: 'NASDAQ post-only order indicator', values: { 'Y': 'Post only — cancel if would take liquidity', 'N': 'Standard order' } },
  9303: { name: 'RoutingInst', desc: 'NYSE Pillar routing instruction', values: { 'N': 'Non-Routable', 'R': 'Routable', 'D': 'Directed (Primary Only)', 'S': 'Directed + Routable', '8': 'Minimum Fill (requires MinQty)', 'A': 'Route to ATS', 'E': 'Route to Algo' } },
  9416: { name: 'ExtendedExecInst', desc: 'NYSE extended execution instruction', values: { '4': 'Retail Order Type 1', '5': 'Retail Order Type 2' } },
  9448: { name: 'IntroducingBadgeID', desc: 'NYSE floor broker badge — required on all floor orders' },
  9479: { name: 'DisplayIndicator', desc: 'Cboe display indicator for hidden orders', values: { 'I': 'Hidden (not displayed)', 'V': 'Visible (displayed)' } },
  9480: { name: 'PreventParticipantMatch', desc: 'Cboe self-match prevention', values: { 'N': 'No prevention', 'Y': 'Prevent match' } },
  9481: { name: 'BaseStrategy', desc: 'Cboe base routing strategy' },
  9483: { name: 'DealID', desc: 'Cboe deal identifier for paired allocations — numeric, unique per pair' },
  9702: { name: 'RouteToBroker', desc: 'NYSE route to floor broker indicator', values: { 'Y': 'Route to floor broker', 'N': 'Do not route to floor broker' } },
  20011: { name: 'RouteToBroker', desc: 'NYSE Texas route to broker indicator' },
};


  const TYPE_LABELS = {
    message: 'Message',
    tag: 'Tag',
    'tag-value': 'Tag',
    enum: 'Enum',
    exchange: 'Exchange',
    tool: 'Tool',
    cert: 'Cert',
    troubleshooting: 'Troubleshooting',
  };

  function safeText(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  /* ── Query parser (for non-expression modes) ── */
  function parseQuery(q) {
    // "tag NN"
    const tagWord = q.match(/^tag\s+(\d+)$/i);
    if (tagWord) return { tagNum: tagWord[1], mode: 'tag' };
    // plain number
    if (/^\d+$/.test(q)) return { tagNum: q, mode: 'num' };
    return { tagNum: null, mode: 'text' };
  }

  /* ── Scorer (used only for non-expression queries) ── */
  function scoreItem(item, q, parsed) {
    let s = 0;
    const titleL  = item.title.toLowerCase();
    const subL    = (item.subtitle || '').toLowerCase();
    const aliases = item.aliases || [];
    const { tagNum, mode } = parsed;

    // Tag number lookup
    if ((mode === 'tag' || mode === 'num') && tagNum) {
      if (item.tag === tagNum) s += 80;
    }

    // Alias exact
    if (aliases.some(a => a === q)) s += 70;

    // Alias starts-with
    if (aliases.some(a => a !== q && a.startsWith(q))) s += 45;

    // Title exact
    if (titleL === q) s += 60;

    // Title starts-with
    if (titleL !== q && titleL.startsWith(q)) s += 35;

    // Title includes (not starts-with)
    if (!titleL.startsWith(q) && titleL.includes(q)) s += 20;

    // Alias partial includes
    if (aliases.some(a => a !== q && !a.startsWith(q) && a.includes(q))) s += 15;

    // Subtitle includes
    if (subL.includes(q)) s += 8;

    return s;
  }

  /* ── Search ── */
  function runSearch(q) {
    if (!q) return [];
    const qL = q.trim().toLowerCase();
    if (!qL) return [];

    // ── FIX expression: tag=value(s) ──────────────────────────────
    const tagEqMatch = q.trim().match(/^(\d+)=(.+)$/);
    if (tagEqMatch) {
      const tagNum = parseInt(tagEqMatch[1]);
      const valueStr = tagEqMatch[2].trim();
      const tagInfo = FIXREADER_TAG_ENUM[tagNum];

      if (tagInfo && tagInfo.values) {
        // Multi-value: "336=1 2 3" → one result per value
        const values = valueStr.split(/\s+/).filter(Boolean);
        const results = [];
        for (const val of values) {
          const valDesc = tagInfo.values[val];
          if (valDesc !== undefined) {
            results.push({
              type: 'tag-value',
              tagNum: tagNum,
              title: safeText(tagInfo.name) + ' = ' + safeText(val) + ' — ' + safeText(valDesc),
              subtitle: 'Tag ' + tagNum + ' · ' + safeText(tagInfo.desc),
              url: '/tag/' + tagNum,
            });
          } else {
            results.push({
              type: 'tag-value',
              tagNum: tagNum,
              title: safeText(tagInfo.name) + ' = ' + safeText(val),
              subtitle: 'Tag ' + tagNum + ' · value not in reference — may be exchange-specific',
              url: '/tag/' + tagNum,
            });
          }
          if (results.length >= 10) break;
        }
        return results;
      }

      // Tag has no values map — fall through to SEARCH_INDEX exact match
      // Only handle clean single values (no embedded spaces)
      if (!/\s/.test(valueStr)) {
        const tagNumStr = String(tagNum);
        const tagVal = valueStr.toLowerCase();

        const exactItems = SEARCH_INDEX.filter(item =>
          item.tag === tagNumStr &&
          item.value != null &&
          item.value.toLowerCase() === tagVal
        );

        if (!exactItems.length) return [];

        const exactSet = new Set(exactItems);

        const relatedTerms = new Set();
        exactItems.forEach(item => {
          if (item.field) relatedTerms.add(item.field.toLowerCase());
          (item.related || []).forEach(r => relatedTerms.add(r.toLowerCase()));
        });

        const related = SEARCH_INDEX
          .filter(item => {
            if (exactSet.has(item)) return false;
            if (item.tag === tagNumStr && item.value != null && item.type !== 'tag') return false;
            return true;
          })
          .map(item => {
            let s = 0;
            const titleL  = item.title.toLowerCase();
            const fieldL  = (item.field || '').toLowerCase();
            const aliases = item.aliases || [];
            if (item.tag === tagNumStr && item.type === 'tag') s += 50;
            for (const r of relatedTerms) {
              if (fieldL === r) s += 30;
              if (aliases.some(a => a === r)) s += 25;
              if (titleL.includes(r)) s += 15;
              else if (aliases.some(a => a.includes(r))) s += 8;
            }
            return { item, s };
          })
          .filter(x => x.s > 0)
          .sort((a, b) => b.s - a.s)
          .slice(0, 10 - exactItems.length)
          .map(x => x.item);

        return [...exactItems, ...related].slice(0, 10);
      }

      return [];
    }

    // ── Broad scoring for all other queries ──────────────────────
    const parsed = parseQuery(qL);
    return SEARCH_INDEX
      .map(item => ({ item, s: scoreItem(item, qL, parsed) }))
      .filter(x => x.s > 0)
      .sort((a, b) => b.s - a.s)
      .slice(0, 10)
      .map(x => x.item);
  }

  /* ── Chip styles (inline, no CSS change needed) ── */
  const CHIP_STYLE = 'font-size:11px;padding:2px 8px;border-radius:4px;border:1px solid #dce3ec;cursor:pointer;background:#f7f9fc;color:#374151;user-select:none';

  /* ── DOM setup ── */
  const input    = document.getElementById('nav-search-input');
  const dropdown = document.getElementById('nav-search-dropdown');
  if (!input || !dropdown) return;

  /* ── Renderer ── */
  function renderResults(results) {
    if (!results.length) {
      dropdown.innerHTML = `<div class="nav-search-empty">No FIXReader results found` +
        `<div style="margin-top:8px;display:flex;gap:6px;flex-wrap:wrap;justify-content:center">` +
        `<span data-chip="35=8" style="${CHIP_STYLE}">Try 35=8</span>` +
        `<span data-chip="Tag 55" style="${CHIP_STYLE}">Try Tag 55</span>` +
        `<span data-chip="IOC" style="${CHIP_STYLE}">Try IOC</span>` +
        `<span data-chip="NYSE session" style="${CHIP_STYLE}">Try NYSE session</span>` +
        `</div></div>`;
      return;
    }
    dropdown.innerHTML = results.map(r => {
      if (r.type === 'tag-value') {
        return `<a class="nav-search-result" href="${r.url}">` +
          `<span class="nav-search-result-title">` +
          `<span class="ml-msg-code" style="font-size:10px;padding:1px 5px;margin-right:6px;vertical-align:middle">${r.tagNum}</span>` +
          `${r.title}</span>` +
          `<span class="nav-search-result-meta">${r.subtitle}</span>` +
          `</a>`;
      }
      const typeLabel = TYPE_LABELS[r.type] || r.type;
      const meta = typeLabel + (r.subtitle ? ' · ' + r.subtitle : '');
      return `<a class="nav-search-result" href="${r.url}">` +
        `<span class="nav-search-result-title">${r.title}</span>` +
        `<span class="nav-search-result-meta">${meta}</span>` +
        `</a>`;
    }).join('');
  }

  let selectedIndex = -1;

  function getResultEls() {
    return Array.from(dropdown.querySelectorAll('.nav-search-result'));
  }

  function setSelected(idx) {
    getResultEls().forEach((el, i) => {
      if (i === idx) {
        el.style.background = 'var(--color-sidebar-bg)';
        el.setAttribute('aria-selected', 'true');
      } else {
        el.style.background = '';
        el.removeAttribute('aria-selected');
      }
    });
    selectedIndex = idx;
  }

  function triggerSearch() {
    const q = input.value.trim();
    selectedIndex = -1;
    if (!q) { dropdown.style.display = 'none'; return; }

    // ── tag=value exact match ──────────────────────────────────
    const exactTagVal = q.match(/^\s*(\d+)\s*=\s*(.+)\s*$/i);
    if (exactTagVal) {
      const tagNum = parseInt(exactTagVal[1]);
      const rawVal = exactTagVal[2].trim();
      const tagInfo = FIXREADER_TAG_ENUM[tagNum];
      const results = [];

      if (tagInfo) {
        const values = rawVal.split(/[\s,]+/).filter(Boolean);
        values.forEach(function(v) {
          const vKey = v.trim();
          const vDesc = tagInfo.values ? (tagInfo.values[vKey] || tagInfo.values[vKey.toUpperCase()] || tagInfo.values[vKey.toLowerCase()] || null) : null;
          results.push({
            type: 'tag-value',
            tagNum: tagNum,
            title: tagInfo.name + ' = ' + vKey + (vDesc ? ' — ' + vDesc : ' — value not in reference'),
            subtitle: 'Tag ' + tagNum + ' · ' + tagInfo.desc,
            url: '/tag/' + tagNum
          });
        });
      } else {
        results.push({
          type: 'tag-value',
          tagNum: tagNum,
          title: 'Tag ' + tagNum + ' = ' + rawVal,
          subtitle: 'Tag ' + tagNum + ' not in FIXReader reference — may be exchange-specific',
          url: '/field-reference'
        });
      }

      if (results.length) {
        renderResults(results);
        dropdown.style.display = 'block';
        return;
      }
    }

    // ── FIX tag number lookup ──────────────────────────────────
    const tagNumMatch = q.match(/^(?:tag\s*)?(\d+)$/i);
    if (tagNumMatch) {
      const tagNum = parseInt(tagNumMatch[1]);
      const tagInfo = FIXREADER_TAG_ENUM[tagNum];
      if (tagInfo) {
        // Show first 5 known values inline when the tag has a values map
        let subtitle = tagInfo.desc;
        if (tagInfo.values) {
          subtitle = Object.entries(tagInfo.values).slice(0, 5)
            .map(([k, v]) => k + ' = ' + v).join(' · ');
        }
        const tagResult = {
          type: 'tag',
          title: 'Tag ' + tagNum + ' — ' + tagInfo.name,
          subtitle: subtitle,
          url: '/tag/' + tagNum,
        };
        const existingResults = SEARCH_INDEX.filter(item =>
          item.aliases && item.aliases.some(a => a.includes(q))
        ).slice(0, 7);
        const allResults = [tagResult, ...existingResults];
        renderResults(allResults);
        dropdown.style.display = 'block';
        return;
      }
    }

    renderResults(runSearch(q));
    dropdown.style.display = 'block';
  }

  input.addEventListener('input', triggerSearch);

  /* Chip click delegation */
  dropdown.addEventListener('click', function(e) {
    const chip = e.target.closest('[data-chip]');
    if (chip) {
      e.preventDefault();
      input.value = chip.dataset.chip;
      triggerSearch();
      input.focus();
    }
  });

  /* Click outside to close */
  document.addEventListener('click', function(e) {
    const wrap = document.getElementById('nav-search-wrap');
    if (wrap && !wrap.contains(e.target)) {
      dropdown.style.display = 'none';
      selectedIndex = -1;
    }
  });

  /* Arrow key navigation + Enter + Escape */
  input.addEventListener('keydown', function(e) {
    if (dropdown.style.display === 'none') return;
    const els = getResultEls();
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelected(Math.min(selectedIndex + 1, els.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelected(Math.max(selectedIndex - 1, -1));
    } else if (e.key === 'Enter') {
      const target = selectedIndex >= 0 ? els[selectedIndex] : els[0];
      if (target) window.location = target.href;
    } else if (e.key === 'Escape') {
      dropdown.style.display = 'none';
      selectedIndex = -1;
      input.blur();
    }
  });

  /* Global ⌘F / Ctrl+F shortcut */
  document.addEventListener('keydown', function(e) {
    if ((e.metaKey || e.ctrlKey) && e.key === 'f') {
      const active = document.activeElement;
      if (active && active !== input && (
        active.tagName === 'INPUT' ||
        active.tagName === 'TEXTAREA' ||
        active.isContentEditable ||
        active.classList.contains('editor-input') ||
        active.classList.contains('cmp-textarea') ||
        active.classList.contains('val-textarea') ||
        active.classList.contains('bld-input')
      )) return;
      e.preventDefault();
      input.focus();
      input.select();
    }
  });

  /* Platform-aware kbd label */
  const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
  const kbd = document.getElementById('nav-search-kbd');
  if (kbd) kbd.textContent = isMac ? '⌘F' : 'Ctrl F';

})();
