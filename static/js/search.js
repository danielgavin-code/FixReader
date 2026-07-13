/* ── FIXReader Search ─────────────────────────────────────────── */

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
  { type:'troubleshooting', title:'Order Rejects', subtitle:'Troubleshooting', url:'/troubleshooting/rejects', aliases:['order rejects','reject','execution report reject','ordstatus 8'] },
  { type:'troubleshooting', title:'Duplicate Orders', subtitle:'Troubleshooting', url:'/troubleshooting/duplicate-orders', aliases:['duplicate orders','duplicate clordid','duplicate order','resend order'] },
  { type:'troubleshooting', title:'Gap Fill & Resend', subtitle:'Troubleshooting', url:'/troubleshooting/gap-fill', aliases:['gap fill','resend request','sequence gap','missing messages'] },
];

(function() {

  const TYPE_LABELS = {
    message: 'Message',
    tag: 'Tag',
    enum: 'Enum',
    exchange: 'Exchange',
    tool: 'Tool',
    cert: 'Cert',
    troubleshooting: 'Troubleshooting',
  };

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

    // ── Exact FIX expression: NN=VV ──────────────────────────────
    const exactMatch = qL.match(/^\s*(\d+)\s*=\s*([a-z0-9._-]+)\s*$/i);
    if (exactMatch) {
      const tagNum = exactMatch[1];
      const tagVal = exactMatch[2]; // already lowercase (qL is lowercased)

      // Step 1: exact tag+value matches (case-insensitive value compare)
      const exactItems = SEARCH_INDEX.filter(item =>
        item.tag === tagNum &&
        item.value != null &&
        item.value.toLowerCase() === tagVal
      );

      if (!exactItems.length) return [];

      const exactSet = new Set(exactItems);

      // Step 2: collect related terms from the matched entries
      const relatedTerms = new Set();
      exactItems.forEach(item => {
        if (item.field) relatedTerms.add(item.field.toLowerCase());
        (item.related || []).forEach(r => relatedTerms.add(r.toLowerCase()));
      });

      // Step 3: find related entries — skip siblings (same tag + has value + not a 'tag' type)
      const related = SEARCH_INDEX
        .filter(item => {
          if (exactSet.has(item)) return false;
          // Skip sibling enum/message entries with a different value on the same tag
          if (item.tag === tagNum && item.value != null && item.type !== 'tag') return false;
          return true;
        })
        .map(item => {
          let s = 0;
          const titleL  = item.title.toLowerCase();
          const fieldL  = (item.field || '').toLowerCase();
          const aliases = item.aliases || [];
          // Tag reference for the matched tag number
          if (item.tag === tagNum && item.type === 'tag') s += 50;
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

  /* ── Renderer ── */
  function renderResults(results) {
    if (!results.length) {
      return `<div class="nav-search-empty">No FIXReader results found` +
        `<div style="margin-top:8px;display:flex;gap:6px;flex-wrap:wrap;justify-content:center">` +
        `<span data-chip="35=8" style="${CHIP_STYLE}">Try 35=8</span>` +
        `<span data-chip="Tag 55" style="${CHIP_STYLE}">Try Tag 55</span>` +
        `<span data-chip="IOC" style="${CHIP_STYLE}">Try IOC</span>` +
        `<span data-chip="NYSE session" style="${CHIP_STYLE}">Try NYSE session</span>` +
        `</div></div>`;
    }
    return results.map(r => {
      const typeLabel = TYPE_LABELS[r.type] || r.type;
      const meta = typeLabel + (r.subtitle ? ' · ' + r.subtitle : '');
      return `<a class="nav-search-result" href="${r.url}">` +
        `<span class="nav-search-result-title">${r.title}</span>` +
        `<span class="nav-search-result-meta">${meta}</span>` +
        `</a>`;
    }).join('');
  }

  /* ── DOM setup ── */
  const input    = document.getElementById('nav-search-input');
  const dropdown = document.getElementById('nav-search-dropdown');
  if (!input || !dropdown) return;

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
    dropdown.innerHTML = renderResults(runSearch(q));
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
