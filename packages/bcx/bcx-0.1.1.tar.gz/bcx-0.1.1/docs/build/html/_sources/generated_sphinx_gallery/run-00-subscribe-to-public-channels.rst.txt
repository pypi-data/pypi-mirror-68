.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_generated_sphinx_gallery_run-00-subscribe-to-public-channels.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_generated_sphinx_gallery_run-00-subscribe-to-public-channels.py:


============================
Subscribe to Public channels
============================

.. contents:: Table of Contents
    :local:
    :depth: 1




.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    INFO:root:Established connection to wss://ws.prod.blockchain.info/mercury-gateway/v1/ws
    INFO:root:{"seqnum":0,"event":"subscribed","channel":"heartbeat"}
    INFO:root:{"seqnum":1,"event":"subscribed","channel":"prices","symbol":"BTC-USD","granularity":60}
    INFO:root:{"seqnum":2,"event":"subscribed","channel":"prices","symbol":"ETH-USD","granularity":60}
    INFO:root:{"seqnum":3,"event":"subscribed","channel":"ticker","symbol":"BTC-USD"}
    INFO:root:{"seqnum":4,"event":"snapshot","channel":"ticker","symbol":"BTC-USD","price_24h":9766.9,"volume_24h":823.10118629,"last_trade_price":8495.5}
    INFO:root:{"seqnum":5,"event":"subscribed","channel":"trades","symbol":"BTC-USD"}
    INFO:root:{"seqnum":6,"event":"updated","channel":"trades","symbol":"BTC-USD","timestamp":"2020-05-10T18:33:36.696315Z","side":"buy","qty":5.892E-4,"price":8501.1,"trade_id":"12886314421"}
    INFO:root:{"seqnum":7,"event":"updated","channel":"ticker","symbol":"BTC-USD","last_trade_price":8501.1}
    INFO:root:{"seqnum":8,"event":"updated","channel":"prices","symbol":"BTC-USD","price":[1589135580000,8506.3,8506.3,8495.5,8495.5,5.961E-4]}
    ERROR:websocket:error from callback <function BlockchainWebsocket._wrap_callback.<locals>.wrapped_f at 0x119cfd0e0>: Error running websocket callback: __init__() missing 1 required positional argument: 'granularity'
    INFO:root:{"seqnum":9,"event":"updated","channel":"prices","symbol":"BTC-USD","price":[1589135580000,8506.3,8506.3,8495.5,8501.1,0.0011853]}
    ERROR:websocket:error from callback <function BlockchainWebsocket._wrap_callback.<locals>.wrapped_f at 0x119cfd0e0>: Error running websocket callback: __init__() missing 1 required positional argument: 'granularity'
    [HeartbeatChannel(is_subscribed=True),
     PricesChannel(symbol=BTC-USD, granularity=60, is_subscribed=True),
     PricesChannel(symbol=ETH-USD, granularity=60, is_subscribed=True),
     TickerChannel(symbol=BTC-USD, is_subscribed=True),
     TradesChannel(symbol=BTC-USD, is_subscribed=True)]
    INFO:root:{"seqnum":10,"event":"subscribed","channel":"symbols"}
    INFO:root:{"seqnum":11,"event":"snapshot","channel":"symbols","symbols":{"BTC-PAX":{"base_currency":"BTC","base_currency_scale":8,"counter_currency":"PAX","counter_currency_scale":8,"min_price_increment":10000000,"min_price_increment_scale":8,"min_order_size":50000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"closed","id":16,"auction_price":0.0,"auction_size":0.0,"auction_time":"","imbalance":0.0},"LTC-BTC":{"base_currency":"LTC","base_currency_scale":8,"counter_currency":"BTC","counter_currency_scale":8,"min_price_increment":100,"min_price_increment_scale":8,"min_order_size":8800000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"closed","id":23,"auction_price":0.0,"auction_size":0.0,"auction_time":"","imbalance":0.0},"ETH-PAX":{"base_currency":"ETH","base_currency_scale":8,"counter_currency":"PAX","counter_currency_scale":8,"min_price_increment":1000000,"min_price_increment_scale":8,"min_order_size":2200000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"closed","id":17,"auction_price":0.0,"auction_size":0.0,"auction_time":"","imbalance":0.0},"XLM-EUR":{"base_currency":"XLM","base_currency_scale":7,"counter_currency":"EUR","counter_currency_scale":2,"min_price_increment":1,"min_price_increment_scale":5,"min_order_size":700000000,"min_order_size_scale":7,"max_order_size":0,"max_order_size_scale":7,"lot_size":1,"lot_size_scale":7,"status":"open","id":11,"auction_price":0.06515,"auction_size":0.0,"auction_time":"0","imbalance":-46670.22},"ALGO-BTC":{"base_currency":"ALGO","base_currency_scale":6,"counter_currency":"BTC","counter_currency_scale":8,"min_price_increment":1,"min_price_increment_scale":8,"min_order_size":20000000,"min_order_size_scale":6,"max_order_size":0,"max_order_size_scale":6,"lot_size":1,"lot_size_scale":6,"status":"open","id":30,"auction_price":2.542E-5,"auction_size":0.0,"auction_time":"0","imbalance":-20363.27},"XLM-BTC":{"base_currency":"XLM","base_currency_scale":7,"counter_currency":"BTC","counter_currency_scale":8,"min_price_increment":1,"min_price_increment_scale":8,"min_order_size":720000000,"min_order_size_scale":7,"max_order_size":0,"max_order_size_scale":7,"lot_size":1,"lot_size_scale":7,"status":"closed","id":12,"auction_price":0.0,"auction_size":0.0,"auction_time":"","imbalance":0.0},"BCH-USDT":{"base_currency":"BCH","base_currency_scale":8,"counter_currency":"USDT","counter_currency_scale":6,"min_price_increment":1000000,"min_price_increment_scale":8,"min_order_size":1800000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"closed","id":28,"auction_price":0.0,"auction_size":0.0,"auction_time":"","imbalance":0.0},"ALGO-USDT":{"base_currency":"ALGO","base_currency_scale":6,"counter_currency":"USDT","counter_currency_scale":6,"min_price_increment":1,"min_price_increment_scale":4,"min_order_size":20000000,"min_order_size_scale":6,"max_order_size":0,"max_order_size_scale":6,"lot_size":1,"lot_size_scale":6,"status":"closed","id":32,"auction_price":0.0,"auction_size":0.0,"auction_time":"","imbalance":0.0},"BTC-GBP":{"base_currency":"BTC","base_currency_scale":8,"counter_currency":"GBP","counter_currency_scale":2,"min_price_increment":10,"min_price_increment_scale":2,"min_order_size":70000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"open","id":35,"auction_price":0.0,"auction_size":0.0,"auction_time":"0","imbalance":0.0},"PAX-USD":{"base_currency":"PAX","base_currency_scale":8,"counter_currency":"USD","counter_currency_scale":2,"min_price_increment":1,"min_price_increment_scale":4,"min_order_size":500000000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":10000,"lot_size_scale":8,"status":"open","id":14,"auction_price":1.0002,"auction_size":0.0,"auction_time":"0","imbalance":-30000.0},"BCH-USD":{"base_currency":"BCH","base_currency_scale":8,"counter_currency":"USD","counter_currency_scale":2,"min_price_increment":1,"min_price_increment_scale":2,"min_order_size":1800000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"open","id":6,"auction_price":255.92,"auction_size":0.0,"auction_time":"0","imbalance":19.4},"LTC-USDT":{"base_currency":"LTC","base_currency_scale":8,"counter_currency":"USDT","counter_currency_scale":6,"min_price_increment":1,"min_price_increment_scale":2,"min_order_size":8800000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"closed","id":29,"auction_price":0.0,"auction_size":0.0,"auction_time":"","imbalance":0.0},"LTC-TRY":{"base_currency":"LTC","base_currency_scale":8,"counter_currency":"TRY","counter_currency_scale":2,"min_price_increment":10,"min_price_increment_scale":2,"min_order_size":8800000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"closed","id":40,"auction_price":0.0,"auction_size":0.0,"auction_time":"","imbalance":0.0},"BTC-EUR":{"base_currency":"BTC","base_currency_scale":8,"counter_currency":"EUR","counter_currency_scale":2,"min_price_increment":10,"min_price_increment_scale":2,"min_order_size":50000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"open","id":4,"auction_price":7985.5,"auction_size":0.0,"auction_time":"0","imbalance":1.72},"USDT-EUR":{"base_currency":"USDT","base_currency_scale":6,"counter_currency":"EUR","counter_currency_scale":2,"min_price_increment":10000,"min_price_increment_scale":8,"min_order_size":500000000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":10000,"lot_size_scale":8,"status":"open","id":25,"auction_price":0.0,"auction_size":0.0,"auction_time":"0","imbalance":0.0},"DGLD-USD":{"base_currency":"DGLD","base_currency_scale":8,"counter_currency":"USD","counter_currency_scale":2,"min_price_increment":1,"min_price_increment_scale":2,"min_order_size":3500000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"open","id":33,"auction_price":0.0,"auction_size":0.0,"auction_time":"","imbalance":0.0},"BCH-PAX":{"base_currency":"BCH","base_currency_scale":8,"counter_currency":"PAX","counter_currency_scale":8,"min_price_increment":1000000,"min_price_increment_scale":8,"min_order_size":1800000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"closed","id":18,"auction_price":0.0,"auction_size":0.0,"auction_time":"","imbalance":0.0},"ETH-USD":{"base_currency":"ETH","base_currency_scale":8,"counter_currency":"USD","counter_currency_scale":2,"min_price_increment":1,"min_price_increment_scale":2,"min_order_size":2200000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"open","id":2,"auction_price":0.0,"auction_size":0.0,"auction_time":"0","imbalance":0.0},"LTC-EUR":{"base_currency":"LTC","base_currency_scale":8,"counter_currency":"EUR","counter_currency_scale":2,"min_price_increment":1,"min_price_increment_scale":2,"min_order_size":8800000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"open","id":21,"auction_price":44.36,"auction_size":0.0,"auction_time":"0","imbalance":72.33},"XLM-PAX":{"base_currency":"XLM","base_currency_scale":7,"counter_currency":"PAX","counter_currency_scale":8,"min_price_increment":1000,"min_price_increment_scale":8,"min_order_size":720000000,"min_order_size_scale":7,"max_order_size":0,"max_order_size_scale":7,"lot_size":1,"lot_size_scale":7,"status":"closed","id":19,"auction_price":0.0,"auction_size":0.0,"auction_time":"","imbalance":0.0},"XLM-USD":{"base_currency":"XLM","base_currency_scale":7,"counter_currency":"USD","counter_currency_scale":2,"min_price_increment":1,"min_price_increment_scale":5,"min_order_size":720000000,"min_order_size_scale":7,"max_order_size":0,"max_order_size_scale":7,"lot_size":1,"lot_size_scale":7,"status":"open","id":10,"auction_price":0.07089,"auction_size":0.0,"auction_time":"0","imbalance":-47819.81},"ETH-BTC":{"base_currency":"ETH","base_currency_scale":8,"counter_currency":"BTC","counter_currency_scale":8,"min_price_increment":100,"min_price_increment_scale":8,"min_order_size":2200000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"open","id":3,"auction_price":0.024584,"auction_size":0.0,"auction_time":"0","imbalance":46.637},"LTC-PAX":{"base_currency":"LTC","base_currency_scale":8,"counter_currency":"PAX","counter_currency_scale":8,"min_price_increment":1,"min_price_increment_scale":2,"min_order_size":8800000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"closed","id":22,"auction_price":0.0,"auction_size":0.0,"auction_time":"","imbalance":0.0},"DGLD-BTC":{"base_currency":"DGLD","base_currency_scale":8,"counter_currency":"BTC","counter_currency_scale":8,"min_price_increment":100,"min_price_increment_scale":8,"min_order_size":3500000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"open","id":34,"auction_price":0.019378,"auction_size":0.0,"auction_time":"0","imbalance":132.0},"PAX-EUR":{"base_currency":"PAX","base_currency_scale":8,"counter_currency":"EUR","counter_currency_scale":2,"min_price_increment":1,"min_price_increment_scale":4,"min_order_size":500000000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":10000,"lot_size_scale":8,"status":"closed","id":15,"auction_price":0.0,"auction_size":0.0,"auction_time":"","imbalance":0.0},"BTC-USDT":{"base_currency":"BTC","base_currency_scale":8,"counter_currency":"USDT","counter_currency_scale":6,"min_price_increment":1,"min_price_increment_scale":2,"min_order_size":50000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"open","id":26,"auction_price":0.0,"auction_size":0.0,"auction_time":"0","imbalance":0.0},"BCH-EUR":{"base_currency":"BCH","base_currency_scale":8,"counter_currency":"EUR","counter_currency_scale":2,"min_price_increment":1,"min_price_increment_scale":2,"min_order_size":1800000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"open","id":7,"auction_price":0.0,"auction_size":0.0,"auction_time":"0","imbalance":0.0},"USDT-TRY":{"base_currency":"USDT","base_currency_scale":6,"counter_currency":"TRY","counter_currency_scale":2,"min_price_increment":1,"min_price_increment_scale":2,"min_order_size":500000000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":10000,"lot_size_scale":8,"status":"open","id":39,"auction_price":0.0,"auction_size":0.0,"auction_time":"","imbalance":0.0},"BCH-BTC":{"base_currency":"BCH","base_currency_scale":8,"counter_currency":"BTC","counter_currency_scale":8,"min_price_increment":100,"min_price_increment_scale":8,"min_order_size":2200000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"open","id":8,"auction_price":0.02601,"auction_size":0.0,"auction_time":"0","imbalance":0.16696011},"BTC-USD":{"base_currency":"BTC","base_currency_scale":8,"counter_currency":"USD","counter_currency_scale":2,"min_price_increment":10,"min_price_increment_scale":2,"min_order_size":50000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"open","id":1,"auction_price":8709.9,"auction_size":0.0,"auction_time":"0","imbalance":1.0},"BCH-ETH":{"base_currency":"BCH","base_currency_scale":8,"counter_currency":"ETH","counter_currency_scale":8,"min_price_increment":100,"min_price_increment_scale":8,"min_order_size":2200000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"closed","id":9,"auction_price":0.0,"auction_size":0.0,"auction_time":"","imbalance":0.0},"ETH-TRY":{"base_currency":"ETH","base_currency_scale":8,"counter_currency":"TRY","counter_currency_scale":2,"min_price_increment":10,"min_price_increment_scale":2,"min_order_size":2200000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"open","id":38,"auction_price":0.0,"auction_size":0.0,"auction_time":"","imbalance":0.0},"USDT-USD":{"base_currency":"USDT","base_currency_scale":6,"counter_currency":"USD","counter_currency_scale":2,"min_price_increment":10000,"min_price_increment_scale":8,"min_order_size":500000000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":10000,"lot_size_scale":8,"status":"open","id":24,"auction_price":0.0,"auction_size":0.0,"auction_time":"0","imbalance":0.0},"ETH-USDT":{"base_currency":"ETH","base_currency_scale":8,"counter_currency":"USDT","counter_currency_scale":6,"min_price_increment":1,"min_price_increment_scale":2,"min_order_size":2200000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"open","id":27,"auction_price":0.0,"auction_size":0.0,"auction_time":"0","imbalance":0.0},"LTC-USD":{"base_currency":"LTC","base_currency_scale":8,"counter_currency":"USD","counter_currency_scale":2,"min_price_increment":1,"min_price_increment_scale":2,"min_order_size":8800000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"open","id":20,"auction_price":48.42,"auction_size":0.0,"auction_time":"0","imbalance":-29.9},"BTC-TRY":{"base_currency":"BTC","base_currency_scale":8,"counter_currency":"TRY","counter_currency_scale":2,"min_price_increment":100,"min_price_increment_scale":2,"min_order_size":50000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"open","id":37,"auction_price":0.0,"auction_size":0.0,"auction_time":"","imbalance":0.0},"ALGO-USD":{"base_currency":"ALGO","base_currency_scale":6,"counter_currency":"USD","counter_currency_scale":2,"min_price_increment":1,"min_price_increment_scale":4,"min_order_size":20000000,"min_order_size_scale":6,"max_order_size":0,"max_order_size_scale":6,"lot_size":1,"lot_size_scale":6,"status":"open","id":31,"auction_price":0.2207,"auction_size":0.0,"auction_time":"0","imbalance":20361.0},"ETH-EUR":{"base_currency":"ETH","base_currency_scale":8,"counter_currency":"EUR","counter_currency_scale":2,"min_price_increment":1,"min_price_increment_scale":2,"min_order_size":2200000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"open","id":5,"auction_price":196.6,"auction_size":0.0,"auction_time":"0","imbalance":69.971},"ETH-GBP":{"base_currency":"ETH","base_currency_scale":8,"counter_currency":"GBP","counter_currency_scale":2,"min_price_increment":1,"min_price_increment_scale":2,"min_order_size":3500000,"min_order_size_scale":8,"max_order_size":0,"max_order_size_scale":8,"lot_size":1,"lot_size_scale":8,"status":"open","id":36,"auction_price":173.3,"auction_size":0.0,"auction_time":"0","imbalance":-69.97},"XLM-ETH":{"base_currency":"XLM","base_currency_scale":7,"counter_currency":"ETH","counter_currency_scale":8,"min_price_increment":1,"min_price_increment_scale":8,"min_order_size":720000000,"min_order_size_scale":7,"max_order_size":0,"max_order_size_scale":7,"lot_size":1,"lot_size_scale":7,"status":"closed","id":13,"auction_price":0.0,"auction_size":0.0,"auction_time":"","imbalance":0.0}}}
    INFO:root:{"seqnum":12,"event":"updated","channel":"heartbeat","timestamp":"2020-05-10T18:33:40.673134Z"}
    [HeartbeatChannel(is_subscribed=True),
     PricesChannel(symbol=BTC-USD, granularity=60, is_subscribed=True),
     PricesChannel(symbol=ETH-USD, granularity=60, is_subscribed=True),
     SymbolsChannel(is_subscribed=True),
     TickerChannel(symbol=BTC-USD, is_subscribed=True),
     TradesChannel(symbol=BTC-USD, is_subscribed=True)]
    INFO:root:{"seqnum":13,"event":"subscribed","channel":"l2","symbol":"BTC-USD"}
    INFO:root:{"seqnum":14,"event":"snapshot","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":0.2,"qty":1.0},{"num":1,"px":1.0,"qty":600.0},{"num":2,"px":4.4,"qty":10.56199279},{"num":1,"px":5.0,"qty":5.0656E-4},{"num":2,"px":6.0,"qty":0.00157635},{"num":1,"px":6.6,"qty":9.8433E-4},{"num":1,"px":9.5,"qty":0.00141542},{"num":1,"px":15.0,"qty":0.00188792},{"num":1,"px":15.3,"qty":0.00252606},{"num":1,"px":48.0,"qty":0.0065},{"num":1,"px":48.4,"qty":0.00660308},{"num":1,"px":90.0,"qty":56.03086906},{"num":1,"px":113.0,"qty":0.01133917},{"num":1,"px":117.0,"qty":2.0035},{"num":1,"px":201.0,"qty":2.95756139},{"num":1,"px":500.0,"qty":0.2},{"num":1,"px":875.0,"qty":0.02},{"num":1,"px":989.0,"qty":0.00218992},{"num":6,"px":1000.0,"qty":2.59386178},{"num":2,"px":1200.0,"qty":5.89097763},{"num":1,"px":1250.0,"qty":0.07565798},{"num":1,"px":2500.0,"qty":0.04742191},{"num":1,"px":2750.0,"qty":30.0},{"num":1,"px":2960.1,"qty":0.01839091},{"num":1,"px":2990.0,"qty":0.03},{"num":2,"px":3000.0,"qty":60.1},{"num":1,"px":3250.0,"qty":30.0},{"num":1,"px":3490.0,"qty":0.03},{"num":3,"px":3500.0,"qty":30.39590183},{"num":1,"px":3512.4,"qty":0.00502719},{"num":1,"px":3850.0,"qty":0.39761226},{"num":1,"px":3880.0,"qty":0.03},{"num":1,"px":3900.0,"qty":55.56629186},{"num":1,"px":4002.0,"qty":0.20167124},{"num":1,"px":4123.0,"qty":0.70873878},{"num":1,"px":4303.0,"qty":0.025},{"num":3,"px":4500.0,"qty":2.96121857},{"num":1,"px":4501.0,"qty":0.06},{"num":1,"px":4721.0,"qty":5.0001E-4},{"num":1,"px":4750.0,"qty":0.53220174},{"num":1,"px":4810.0,"qty":1.25754635},{"num":1,"px":4823.0,"qty":0.02343935},{"num":1,"px":4890.0,"qty":0.02},{"num":4,"px":4900.0,"qty":1.672},{"num":4,"px":5000.0,"qty":0.47514295},{"num":1,"px":5100.0,"qty":0.00256637},{"num":1,"px":5102.0,"qty":0.01},{"num":3,"px":5200.0,"qty":0.10568659},{"num":1,"px":5300.0,"qty":0.02282057},{"num":1,"px":5346.0,"qty":0.015},{"num":1,"px":5555.0,"qty":0.01942401},{"num":3,"px":5600.0,"qty":0.32397771},{"num":1,"px":5669.0,"qty":0.26326443},{"num":1,"px":5699.9,"qty":0.03},{"num":2,"px":5700.0,"qty":0.020067},{"num":1,"px":5867.0,"qty":0.015},{"num":1,"px":5900.0,"qty":0.4},{"num":1,"px":5999.9,"qty":0.03},{"num":3,"px":6000.0,"qty":0.10879163},{"num":1,"px":6010.0,"qty":0.01},{"num":1,"px":6045.0,"qty":0.00437656},{"num":1,"px":6100.0,"qty":0.14145804},{"num":1,"px":6200.0,"qty":0.03},{"num":1,"px":6210.0,"qty":0.03219308},{"num":1,"px":6270.0,"qty":5.0001E-4},{"num":1,"px":6300.0,"qty":0.01},{"num":1,"px":6350.0,"qty":0.14523642},{"num":1,"px":6375.0,"qty":0.11800473},{"num":3,"px":6400.0,"qty":1.21},{"num":2,"px":6500.0,"qty":0.32195538},{"num":2,"px":6501.0,"qty":0.04},{"num":1,"px":6528.6,"qty":0.30479471},{"num":3,"px":6600.0,"qty":0.06040989},{"num":1,"px":6601.0,"qty":0.01},{"num":1,"px":6650.0,"qty":0.082509},{"num":1,"px":6750.0,"qty":0.2},{"num":3,"px":6800.0,"qty":0.00684454},{"num":1,"px":6801.0,"qty":0.01},{"num":1,"px":6820.0,"qty":0.2},{"num":1,"px":6890.0,"qty":0.2},{"num":1,"px":6893.0,"qty":0.01448133},{"num":1,"px":6900.0,"qty":0.0015},{"num":1,"px":6901.0,"qty":0.01},{"num":1,"px":6905.0,"qty":0.2},{"num":1,"px":6955.0,"qty":0.2},{"num":11,"px":7000.0,"qty":2.92368165},{"num":1,"px":7005.0,"qty":0.29208246},{"num":1,"px":7050.0,"qty":0.02},{"num":1,"px":7055.0,"qty":0.2},{"num":2,"px":7100.0,"qty":0.01455824},{"num":1,"px":7121.0,"qty":0.02},{"num":1,"px":7130.0,"qty":0.016589},{"num":4,"px":7200.0,"qty":1.0074776},{"num":1,"px":7250.0,"qty":0.00152323},{"num":2,"px":7300.0,"qty":0.0312},{"num":1,"px":7350.0,"qty":0.39706244},{"num":3,"px":7400.0,"qty":0.23440512},{"num":7,"px":7500.0,"qty":0.31443201},{"num":1,"px":7523.0,"qty":0.013414},{"num":3,"px":7600.0,"qty":0.00421943},{"num":1,"px":7601.0,"qty":0.01},{"num":1,"px":7700.0,"qty":0.002},{"num":1,"px":7701.0,"qty":0.01},{"num":1,"px":7770.0,"qty":0.01652775},{"num":4,"px":7800.0,"qty":0.26757398},{"num":2,"px":7850.0,"qty":0.03952079},{"num":1,"px":7900.0,"qty":0.07},{"num":1,"px":7901.0,"qty":0.01},{"num":1,"px":7950.0,"qty":8.2044E-4},{"num":8,"px":8000.0,"qty":0.12771649},{"num":3,"px":8100.0,"qty":0.82676551},{"num":1,"px":8153.0,"qty":0.01310229},{"num":1,"px":8170.0,"qty":0.2355617},{"num":1,"px":8200.0,"qty":0.2},{"num":2,"px":8250.0,"qty":0.31492472},{"num":1,"px":8293.2,"qty":5.0001E-4},{"num":2,"px":8300.0,"qty":0.3},{"num":2,"px":8350.0,"qty":0.08585365},{"num":1,"px":8372.9,"qty":5.0001E-4},{"num":1,"px":8375.7,"qty":2.14},{"num":1,"px":8426.7,"qty":1.74},{"num":1,"px":8450.0,"qty":0.015},{"num":2,"px":8477.7,"qty":5.179},{"num":1,"px":8482.4,"qty":28.9},{"num":1,"px":8483.6,"qty":3.01},{"num":1,"px":8486.4,"qty":18.9},{"num":1,"px":8487.4,"qty":36.0},{"num":1,"px":8488.6,"qty":2.01},{"num":1,"px":8489.0,"qty":5.0},{"num":1,"px":8489.1,"qty":3.5278},{"num":1,"px":8489.9,"qty":1.7649},{"num":1,"px":8490.6,"qty":1.01},{"num":1,"px":8490.9,"qty":9.8},{"num":1,"px":8491.8,"qty":0.618},{"num":1,"px":8492.3,"qty":1.0}],"asks":[{"num":1,"px":8500.2,"qty":1.01},{"num":1,"px":8501.2,"qty":2.01},{"num":1,"px":8501.9,"qty":0.618},{"num":1,"px":8505.9,"qty":1.0},{"num":1,"px":8506.5,"qty":9.3},{"num":1,"px":8507.2,"qty":3.01},{"num":2,"px":8508.0,"qty":31.8},{"num":1,"px":8508.9,"qty":1.7649},{"num":1,"px":8509.0,"qty":36.0},{"num":1,"px":8509.5,"qty":19.6},{"num":1,"px":8510.0,"qty":49.31},{"num":1,"px":8511.5,"qty":49.22},{"num":1,"px":8515.8,"qty":2.02},{"num":1,"px":8518.3,"qty":3.5284},{"num":1,"px":8545.0,"qty":0.00244816},{"num":1,"px":8566.7,"qty":5.8312063},{"num":1,"px":8566.8,"qty":2.26},{"num":1,"px":8586.0,"qty":0.01},{"num":1,"px":8622.1,"qty":1.78},{"num":2,"px":8750.0,"qty":0.04964799},{"num":1,"px":8825.0,"qty":0.03358068},{"num":1,"px":8844.6,"qty":0.02},{"num":1,"px":8860.0,"qty":0.015},{"num":1,"px":8867.0,"qty":9.99E-4},{"num":1,"px":8875.0,"qty":5.0E-4},{"num":2,"px":8900.0,"qty":0.00598845},{"num":2,"px":8950.0,"qty":0.00803318},{"num":1,"px":8956.0,"qty":0.01},{"num":3,"px":9000.0,"qty":0.24650088},{"num":1,"px":9083.9,"qty":0.0032759},{"num":2,"px":9100.0,"qty":0.00138138},{"num":1,"px":9150.0,"qty":0.00164242},{"num":1,"px":9171.2,"qty":0.00327591},{"num":1,"px":9186.0,"qty":0.01},{"num":4,"px":9200.0,"qty":0.07948726},{"num":1,"px":9302.1,"qty":0.00327593},{"num":1,"px":9453.0,"qty":0.02},{"num":1,"px":9476.9,"qty":0.00327592},{"num":2,"px":9490.0,"qty":0.37121609},{"num":1,"px":9500.0,"qty":7.7488E-4},{"num":1,"px":9502.2,"qty":0.015},{"num":1,"px":9530.0,"qty":0.00550087},{"num":1,"px":9545.0,"qty":0.09462243},{"num":1,"px":9598.0,"qty":5.8E-4},{"num":1,"px":9598.1,"qty":0.015},{"num":5,"px":9600.0,"qty":0.04113314},{"num":1,"px":9624.1,"qty":0.015},{"num":1,"px":9655.0,"qty":5.1E-4},{"num":1,"px":9688.5,"qty":0.015},{"num":2,"px":9700.0,"qty":0.04309463},{"num":1,"px":9724.2,"qty":0.015},{"num":1,"px":9750.0,"qty":0.1},{"num":1,"px":9755.0,"qty":5.1E-4},{"num":1,"px":9788.8,"qty":0.015},{"num":2,"px":9800.0,"qty":0.401},{"num":1,"px":9812.4,"qty":0.01},{"num":1,"px":9818.0,"qty":5.0E-4},{"num":2,"px":9850.0,"qty":0.40679178},{"num":1,"px":9854.1,"qty":0.01},{"num":1,"px":9880.0,"qty":0.0071502},{"num":1,"px":9885.0,"qty":0.01},{"num":1,"px":9893.0,"qty":0.04},{"num":1,"px":9899.0,"qty":0.26176124},{"num":1,"px":9899.5,"qty":0.01},{"num":4,"px":9900.0,"qty":0.03469084},{"num":1,"px":9950.0,"qty":0.01554376},{"num":1,"px":9959.7,"qty":0.01},{"num":1,"px":9975.0,"qty":0.001},{"num":2,"px":9990.0,"qty":0.99792503},{"num":1,"px":9993.1,"qty":0.01},{"num":1,"px":9994.0,"qty":0.01467174},{"num":1,"px":9999.0,"qty":0.00960447},{"num":10,"px":10000.0,"qty":0.30396675},{"num":1,"px":10003.0,"qty":0.08100746},{"num":1,"px":10023.4,"qty":0.01},{"num":1,"px":10025.0,"qty":0.01629675},{"num":1,"px":10036.0,"qty":0.0307},{"num":3,"px":10050.0,"qty":0.06241396},{"num":1,"px":10052.5,"qty":7.702E-4},{"num":1,"px":10060.0,"qty":0.0150765},{"num":1,"px":10065.0,"qty":0.65157008},{"num":1,"px":10068.8,"qty":0.01},{"num":3,"px":10100.0,"qty":0.26071473},{"num":1,"px":10109.0,"qty":0.01},{"num":1,"px":10125.2,"qty":0.01},{"num":1,"px":10189.5,"qty":0.01},{"num":3,"px":10200.0,"qty":0.02208879},{"num":1,"px":10229.3,"qty":0.01},{"num":1,"px":10231.4,"qty":0.00123857},{"num":1,"px":10250.0,"qty":0.001},{"num":1,"px":10289.0,"qty":0.46046664},{"num":1,"px":10289.3,"qty":0.01},{"num":1,"px":10325.0,"qty":0.04},{"num":1,"px":10326.2,"qty":0.01},{"num":1,"px":10333.0,"qty":0.317},{"num":1,"px":10360.0,"qty":0.11735025},{"num":1,"px":10389.5,"qty":0.01},{"num":4,"px":10400.0,"qty":0.0643328},{"num":1,"px":10420.0,"qty":0.02},{"num":5,"px":10500.0,"qty":0.00742601},{"num":1,"px":10507.0,"qty":0.00796566},{"num":1,"px":10539.7,"qty":0.02527625},{"num":1,"px":10550.0,"qty":0.002},{"num":1,"px":10564.0,"qty":0.005},{"num":1,"px":10600.0,"qty":0.0015},{"num":1,"px":10624.0,"qty":0.005},{"num":1,"px":10745.0,"qty":1.0},{"num":1,"px":10785.0,"qty":0.02},{"num":4,"px":10800.0,"qty":0.16614097},{"num":1,"px":10885.0,"qty":0.06},{"num":1,"px":10989.0,"qty":0.005},{"num":1,"px":10990.0,"qty":0.4},{"num":2,"px":10993.0,"qty":0.035},{"num":5,"px":11000.0,"qty":0.52732047},{"num":1,"px":11111.0,"qty":5.0E-4},{"num":1,"px":11200.0,"qty":0.001},{"num":1,"px":11233.0,"qty":0.0026442},{"num":1,"px":11302.0,"qty":0.01},{"num":1,"px":11364.0,"qty":0.005},{"num":1,"px":11400.0,"qty":0.00114808},{"num":1,"px":11420.0,"qty":0.01332208},{"num":2,"px":11500.0,"qty":0.12864227},{"num":1,"px":11600.0,"qty":0.002},{"num":1,"px":11786.0,"qty":0.06},{"num":1,"px":11800.0,"qty":5.996E-4},{"num":1,"px":11844.0,"qty":0.01},{"num":1,"px":11893.0,"qty":0.01},{"num":3,"px":12000.0,"qty":0.85104442},{"num":1,"px":12222.0,"qty":5.0E-4},{"num":1,"px":12246.0,"qty":0.08174803},{"num":2,"px":12300.0,"qty":1.01},{"num":1,"px":12500.0,"qty":0.00130199},{"num":1,"px":13333.0,"qty":5.0E-4},{"num":1,"px":13420.0,"qty":0.02},{"num":1,"px":13498.0,"qty":0.5},{"num":1,"px":14000.0,"qty":0.01},{"num":1,"px":14444.0,"qty":5.0E-4},{"num":1,"px":15000.0,"qty":0.06},{"num":1,"px":15525.0,"qty":0.50095482},{"num":1,"px":15555.0,"qty":5.0E-4},{"num":1,"px":16110.6,"qty":0.00327592},{"num":1,"px":16666.0,"qty":5.0E-4},{"num":1,"px":17495.8,"qty":0.00232965},{"num":1,"px":17777.0,"qty":5.0E-4},{"num":1,"px":18888.0,"qty":5.0E-4},{"num":1,"px":19000.0,"qty":0.01618178},{"num":1,"px":19359.7,"qty":0.0130365},{"num":1,"px":19999.0,"qty":5.0E-4},{"num":1,"px":20000.0,"qty":0.07212326},{"num":1,"px":21111.0,"qty":5.0E-4},{"num":1,"px":21860.9,"qty":0.1},{"num":1,"px":22222.0,"qty":5.0E-4},{"num":1,"px":23112.0,"qty":7.2965E-4},{"num":1,"px":23333.0,"qty":5.0E-4},{"num":1,"px":24444.0,"qty":5.0E-4},{"num":1,"px":25550.0,"qty":0.00116427},{"num":1,"px":25555.0,"qty":5.0E-4},{"num":1,"px":26666.0,"qty":5.0E-4},{"num":1,"px":27008.0,"qty":9.2965E-4},{"num":1,"px":27777.0,"qty":5.0E-4},{"num":1,"px":28888.0,"qty":5.0E-4},{"num":1,"px":29673.7,"qty":0.010005},{"num":1,"px":29999.0,"qty":5.0E-4},{"num":1,"px":30000.0,"qty":0.83727024},{"num":1,"px":30003.0,"qty":6.2965E-4},{"num":1,"px":31111.0,"qty":5.0E-4},{"num":1,"px":31653.7,"qty":5.0001E-4},{"num":1,"px":32222.3,"qty":0.00211112},{"num":1,"px":33953.6,"qty":0.00147337},{"num":1,"px":35000.7,"qty":0.00146498},{"num":1,"px":50000.0,"qty":0.33270952},{"num":1,"px":64733.0,"qty":0.01229168},{"num":1,"px":200000.0,"qty":0.00540601},{"num":1,"px":954200.0,"qty":6.0279E-4},{"num":1,"px":964200.0,"qty":6.0E-4},{"num":1,"px":969700.0,"qty":5.9839E-4}]}
    INFO:root:{"seqnum":15,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8513.8,"qty":3.5303}]}
    INFO:root:{"seqnum":16,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8492.5,"qty":0.124}],"asks":[]}
    INFO:root:{"seqnum":17,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8498.4,"qty":0.124}]}
    INFO:root:{"seqnum":18,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8506.5,"qty":0.0}]}
    INFO:root:{"seqnum":19,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8505.0,"qty":9.3}]}
    INFO:root:{"seqnum":20,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8622.1,"qty":0.0}]}
    INFO:root:{"seqnum":21,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8616.1,"qty":1.78}]}
    INFO:root:{"seqnum":22,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8492.5,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":23,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8498.4,"qty":0.0}]}
    INFO:root:{"seqnum":24,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8491.8,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":25,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8501.9,"qty":0.0}]}
    INFO:root:{"seqnum":26,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8492.1,"qty":0.124}],"asks":[]}
    INFO:root:{"seqnum":27,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8509.5,"qty":0.0}]}
    INFO:root:{"seqnum":28,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8507.0,"qty":19.6}]}
    INFO:root:{"seqnum":29,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8498.0,"qty":0.124}]}
    INFO:root:{"seqnum":30,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":2,"px":8490.6,"qty":1.628}],"asks":[]}
    INFO:root:{"seqnum":31,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8500.7,"qty":0.618}]}
    INFO:root:{"seqnum":32,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8492.3,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":33,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":2,"px":8492.1,"qty":1.124}],"asks":[]}
    INFO:root:{"seqnum":34,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8492.1,"qty":1.0}],"asks":[]}
    INFO:root:{"seqnum":35,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8498.0,"qty":0.0}]}
    INFO:root:{"seqnum":36,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8486.4,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":37,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8487.4,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":38,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8483.9,"qty":18.9}],"asks":[]}
    INFO:root:{"seqnum":39,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8484.4,"qty":36.0}],"asks":[]}
    INFO:root:{"seqnum":40,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.6,"qty":0.124}],"asks":[]}
    INFO:root:{"seqnum":41,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8497.5,"qty":0.124}]}
    INFO:root:{"seqnum":42,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8505.0,"qty":0.0}]}
    INFO:root:{"seqnum":43,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8503.5,"qty":9.3}]}
    INFO:root:{"seqnum":44,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8509.0,"qty":0.0}]}
    INFO:root:{"seqnum":45,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8506.5,"qty":36.0}]}
    INFO:root:{"seqnum":46,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8508.0,"qty":5.0}]}
    INFO:root:{"seqnum":47,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":2,"px":8506.5,"qty":62.8}]}
    INFO:root:{"seqnum":48,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8510.0,"qty":0.0}]}
    INFO:root:{"seqnum":49,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8507.5,"qty":49.31}]}
    INFO:root:{"seqnum":50,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8511.5,"qty":0.0}]}
    INFO:root:{"seqnum":51,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8509.0,"qty":49.22}]}
    INFO:root:{"seqnum":52,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8506.5,"qty":36.0}]}
    INFO:root:{"seqnum":53,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8505.0,"qty":26.8}]}
    INFO:root:{"seqnum":54,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8509.0,"qty":0.0}]}
    INFO:root:{"seqnum":55,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8511.5,"qty":49.22}]}
    INFO:root:{"seqnum":56,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8492.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":57,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.1,"qty":1.0}],"asks":[]}
    INFO:root:{"seqnum":58,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8490.9,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":59,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8489.4,"qty":9.8}],"asks":[]}
    [HeartbeatChannel(is_subscribed=True),
     OrderbookL2Channel(symbol=BTC-USD, is_subscribed=True),
     PricesChannel(symbol=BTC-USD, granularity=60, is_subscribed=True),
     PricesChannel(symbol=ETH-USD, granularity=60, is_subscribed=True),
     SymbolsChannel(is_subscribed=True),
     TickerChannel(symbol=BTC-USD, is_subscribed=True),
     TradesChannel(symbol=BTC-USD, is_subscribed=True)]
    INFO:root:{"seqnum":60,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8491.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":61,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8505.9,"qty":0.0}]}
    INFO:root:{"seqnum":62,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":2,"px":8491.6,"qty":1.124}],"asks":[]}
    INFO:root:{"seqnum":63,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8505.2,"qty":1.0}]}
    INFO:root:{"seqnum":64,"event":"updated","channel":"heartbeat","timestamp":"2020-05-10T18:33:45.773809Z"}
    INFO:root:{"seqnum":65,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.6,"qty":1.0}],"asks":[]}
    INFO:root:{"seqnum":66,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8497.5,"qty":0.0}]}
    INFO:root:{"seqnum":67,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.3,"qty":0.124}],"asks":[]}
    INFO:root:{"seqnum":68,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8497.2,"qty":0.124}]}
    INFO:root:{"seqnum":69,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8491.3,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":70,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8497.2,"qty":0.0}]}
    INFO:root:{"seqnum":71,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8500.2,"qty":0.0}]}
    INFO:root:{"seqnum":72,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8501.2,"qty":0.0}]}
    INFO:root:{"seqnum":73,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8504.2,"qty":1.01}]}
    INFO:root:{"seqnum":74,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8506.2,"qty":2.01}]}
    INFO:root:{"seqnum":75,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.8,"qty":0.124}],"asks":[]}
    INFO:root:{"seqnum":76,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8497.7,"qty":0.124}]}
    INFO:root:{"seqnum":77,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8490.6,"qty":0.618}],"asks":[]}
    INFO:root:{"seqnum":78,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8504.2,"qty":0.0}]}
    INFO:root:{"seqnum":79,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":2,"px":8491.6,"qty":2.01}],"asks":[]}
    INFO:root:{"seqnum":80,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8503.2,"qty":1.01}]}
    INFO:root:{"seqnum":81,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.6,"qty":1.0}],"asks":[]}
    INFO:root:{"seqnum":82,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8503.2,"qty":0.0}]}
    INFO:root:{"seqnum":83,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8506.2,"qty":0.0}]}
    INFO:root:{"seqnum":84,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8492.6,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":85,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8501.2,"qty":1.01}]}
    INFO:root:{"seqnum":86,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8504.7,"qty":2.01}]}
    INFO:root:{"seqnum":87,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8505.0,"qty":0.0}]}
    INFO:root:{"seqnum":88,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":2,"px":8506.5,"qty":62.8}]}
    INFO:root:{"seqnum":89,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8501.2,"qty":0.0}]}
    INFO:root:{"seqnum":90,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8502.7,"qty":1.01}]}
    INFO:root:{"seqnum":91,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8491.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":92,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8505.2,"qty":0.0}]}
    INFO:root:{"seqnum":93,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.4,"qty":1.0}],"asks":[]}
    INFO:root:{"seqnum":94,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8504.9,"qty":1.0}]}
    INFO:root:{"seqnum":95,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8492.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":96,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8492.1,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":97,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8502.7,"qty":0.0}]}
    INFO:root:{"seqnum":98,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8502.2,"qty":1.01}]}
    INFO:root:{"seqnum":99,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8492.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":100,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8493.1,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":101,"event":"subscribed","channel":"l3","symbol":"BTC-USD"}
    INFO:root:{"seqnum":102,"event":"snapshot","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430189","px":8493.1,"qty":1.01},{"id":"13649430163","px":8491.8,"qty":0.124},{"id":"13649430180","px":8491.4,"qty":1.0},{"id":"13649430102","px":8490.6,"qty":0.618},{"id":"13649430000","px":8489.9,"qty":1.7649},{"id":"13649430138","px":8489.4,"qty":9.8},{"id":"13649428955","px":8489.1,"qty":3.5278},{"id":"13649430037","px":8489.0,"qty":5.0},{"id":"13649429994","px":8488.6,"qty":2.01},{"id":"13649430115","px":8484.4,"qty":36.0},{"id":"13649430114","px":8483.9,"qty":18.9},{"id":"13649429973","px":8483.6,"qty":3.01},{"id":"13649430044","px":8482.4,"qty":28.9},{"id":"13649430049","px":8477.7,"qty":1.65},{"id":"13649429619","px":8477.7,"qty":3.529},{"id":"13649156362","px":8450.0,"qty":0.015},{"id":"13649430050","px":8426.7,"qty":1.74},{"id":"13649430052","px":8375.7,"qty":2.14},{"id":"13649232785","px":8372.9,"qty":5.0001E-4},{"id":"13649173817","px":8350.0,"qty":0.01623179},{"id":"13649093451","px":8350.0,"qty":0.06962186},{"id":"13649337894","px":8300.0,"qty":0.1},{"id":"13649104799","px":8300.0,"qty":0.2},{"id":"13649232800","px":8293.2,"qty":5.0001E-4},{"id":"13648444846","px":8250.0,"qty":0.11492472},{"id":"13649010691","px":8250.0,"qty":0.2},{"id":"13649011649","px":8200.0,"qty":0.2},{"id":"13649424160","px":8170.0,"qty":0.2355617},{"id":"13648452344","px":8153.0,"qty":0.01310229},{"id":"13649105385","px":8100.0,"qty":0.0661495},{"id":"13649137723","px":8100.0,"qty":0.10558549},{"id":"13649216025","px":8100.0,"qty":0.65503052},{"id":"13645970328","px":8000.0,"qty":5.1E-4},{"id":"13647091110","px":8000.0,"qty":0.00117966},{"id":"13638457648","px":8000.0,"qty":0.00122829},{"id":"13640717226","px":8000.0,"qty":0.0015},{"id":"13638430515","px":8000.0,"qty":0.00435701},{"id":"13649234331","px":8000.0,"qty":0.00503},{"id":"13649149636","px":8000.0,"qty":0.01391153},{"id":"13617321516","px":8000.0,"qty":0.1},{"id":"13608217412","px":7950.0,"qty":8.2044E-4},{"id":"13618885118","px":7901.0,"qty":0.01},{"id":"13647482348","px":7900.0,"qty":0.07},{"id":"13608217825","px":7850.0,"qty":7.2114E-4},{"id":"13649276828","px":7850.0,"qty":0.03879965},{"id":"13646551253","px":7800.0,"qty":9.9504E-4},{"id":"13609365509","px":7800.0,"qty":0.002},{"id":"13613592073","px":7800.0,"qty":0.06457894},{"id":"13647188438","px":7800.0,"qty":0.2},{"id":"13623735571","px":7770.0,"qty":0.01652775},{"id":"13607237126","px":7701.0,"qty":0.01},{"id":"13648011294","px":7700.0,"qty":0.002},{"id":"13607237365","px":7601.0,"qty":0.01},{"id":"13647398088","px":7600.0,"qty":0.001},{"id":"13603296557","px":7600.0,"qty":0.00121943},{"id":"13609363459","px":7600.0,"qty":0.002},{"id":"13641032543","px":7523.0,"qty":0.013414},{"id":"13646133498","px":7500.0,"qty":0.00640326},{"id":"13644020847","px":7500.0,"qty":0.01097891},{"id":"13649002331","px":7500.0,"qty":0.015},{"id":"13608102548","px":7500.0,"qty":0.0302459},{"id":"13649076877","px":7500.0,"qty":0.06573252},{"id":"13648500860","px":7500.0,"qty":0.07},{"id":"13609075559","px":7500.0,"qty":0.11607142},{"id":"13609361494","px":7400.0,"qty":0.002},{"id":"13614992926","px":7400.0,"qty":0.10740512},{"id":"13608051815","px":7400.0,"qty":0.125},{"id":"13646613523","px":7350.0,"qty":0.39706244},{"id":"13592983964","px":7300.0,"qty":0.0012},{"id":"13647355734","px":7300.0,"qty":0.03},{"id":"13633958034","px":7250.0,"qty":0.00152323},{"id":"13592988200","px":7200.0,"qty":8.1242E-4},{"id":"13649316461","px":7200.0,"qty":0.002654},{"id":"13605356253","px":7200.0,"qty":0.00401118},{"id":"13648767456","px":7200.0,"qty":1.0},{"id":"13593311707","px":7130.0,"qty":0.016589},{"id":"13597037628","px":7121.0,"qty":0.02},{"id":"13592920616","px":7100.0,"qty":0.0013},{"id":"13647357230","px":7100.0,"qty":0.01325824},{"id":"13596102936","px":7055.0,"qty":0.2},{"id":"13597028708","px":7050.0,"qty":0.02},{"id":"13596103566","px":7005.0,"qty":0.29208246},{"id":"13612173973","px":7000.0,"qty":5.5E-4},{"id":"13641236610","px":7000.0,"qty":7.1E-4},{"id":"13592934732","px":7000.0,"qty":0.00101755},{"id":"13620801108","px":7000.0,"qty":0.00172178},{"id":"13599728837","px":7000.0,"qty":0.0025},{"id":"13640728466","px":7000.0,"qty":0.04896648},{"id":"13615646127","px":7000.0,"qty":0.0663974},{"id":"13591883483","px":7000.0,"qty":0.1},{"id":"13647387393","px":7000.0,"qty":0.1},{"id":"13606475464","px":7000.0,"qty":0.78031844},{"id":"13608098481","px":7000.0,"qty":1.8215},{"id":"13596102610","px":6955.0,"qty":0.2},{"id":"13596102003","px":6905.0,"qty":0.2},{"id":"13592111459","px":6901.0,"qty":0.01},{"id":"13590257617","px":6900.0,"qty":0.0015},{"id":"13648449374","px":6893.0,"qty":0.01448133},{"id":"13596101216","px":6890.0,"qty":0.2},{"id":"13596100187","px":6820.0,"qty":0.2},{"id":"13592110196","px":6801.0,"qty":0.01},{"id":"13590259980","px":6800.0,"qty":8.0E-4},{"id":"13647655227","px":6800.0,"qty":0.00104454},{"id":"13599725977","px":6800.0,"qty":0.005},{"id":"13596098708","px":6750.0,"qty":0.2},{"id":"13587720558","px":6650.0,"qty":0.082509},{"id":"13592110393","px":6601.0,"qty":0.01},{"id":"13599724832","px":6600.0,"qty":0.005},{"id":"13610316621","px":6600.0,"qty":0.00540989},{"id":"13641952208","px":6600.0,"qty":0.05},{"id":"13647668968","px":6528.6,"qty":0.30479471},{"id":"13592110736","px":6501.0,"qty":0.01},{"id":"13613074375","px":6501.0,"qty":0.03},{"id":"13649010921","px":6500.0,"qty":0.015},{"id":"13626686148","px":6500.0,"qty":0.30695538},{"id":"13553984573","px":6400.0,"qty":0.01},{"id":"13520699900","px":6400.0,"qty":0.2},{"id":"13648768137","px":6400.0,"qty":1.0},{"id":"13600527603","px":6375.0,"qty":0.11800473},{"id":"13648382544","px":6350.0,"qty":0.14523642},{"id":"13528818930","px":6300.0,"qty":0.01},{"id":"13535372529","px":6270.0,"qty":5.0001E-4},{"id":"13638038847","px":6210.0,"qty":0.03219308},{"id":"13613066883","px":6200.0,"qty":0.03},{"id":"13567646350","px":6100.0,"qty":0.14145804},{"id":"13646126142","px":6045.0,"qty":0.00437656},{"id":"13528820477","px":6010.0,"qty":0.01},{"id":"13529508912","px":6000.0,"qty":0.00369112},{"id":"13610317011","px":6000.0,"qty":0.00510051},{"id":"13647388425","px":6000.0,"qty":0.1},{"id":"13613069871","px":5999.9,"qty":0.03},{"id":"13520701336","px":5900.0,"qty":0.4},{"id":"13514646789","px":5867.0,"qty":0.015},{"id":"13538004818","px":5700.0,"qty":0.01},{"id":"13570902726","px":5700.0,"qty":0.010067},{"id":"13613072422","px":5699.9,"qty":0.03},{"id":"13639491384","px":5669.0,"qty":0.26326443},{"id":"13494175453","px":5600.0,"qty":0.00112586},{"id":"13493577076","px":5600.0,"qty":0.01221881},{"id":"13608782642","px":5600.0,"qty":0.31063304},{"id":"13634921494","px":5555.0,"qty":0.01942401},{"id":"13514649449","px":5346.0,"qty":0.015},{"id":"13492965979","px":5300.0,"qty":0.02282057},{"id":"13648061963","px":5200.0,"qty":0.001},{"id":"13538006169","px":5200.0,"qty":0.01030021},{"id":"13605678542","px":5200.0,"qty":0.09438638},{"id":"13489439161","px":5102.0,"qty":0.01},{"id":"13545047900","px":5100.0,"qty":0.00256637},{"id":"13610317845","px":5000.0,"qty":0.00709293},{"id":"13489819771","px":5000.0,"qty":0.01},{"id":"13647389460","px":5000.0,"qty":0.08763117},{"id":"13627254387","px":5000.0,"qty":0.37041885},{"id":"13485386006","px":4900.0,"qty":0.01},{"id":"13580091674","px":4900.0,"qty":0.062},{"id":"13520702169","px":4900.0,"qty":0.6},{"id":"13648768788","px":4900.0,"qty":1.0},{"id":"13593433142","px":4890.0,"qty":0.02},{"id":"13514650078","px":4823.0,"qty":0.02343935},{"id":"13494844226","px":4810.0,"qty":1.25754635},{"id":"13646483313","px":4750.0,"qty":0.53220174},{"id":"13649232831","px":4721.0,"qty":5.0001E-4},{"id":"13492617474","px":4501.0,"qty":0.06},{"id":"13569165229","px":4500.0,"qty":0.030664},{"id":"13647347077","px":4500.0,"qty":0.55555457},{"id":"13606868671","px":4500.0,"qty":2.375},{"id":"13505990538","px":4303.0,"qty":0.025},{"id":"13591073211","px":4123.0,"qty":0.70873878},{"id":"13646642600","px":4002.0,"qty":0.20167124},{"id":"13561946793","px":3900.0,"qty":55.56629186},{"id":"13529528716","px":3880.0,"qty":0.03},{"id":"13647345082","px":3850.0,"qty":0.39761226},{"id":"13459900059","px":3512.4,"qty":0.00502719},{"id":"13614918042","px":3500.0,"qty":0.18758585},{"id":"13478659852","px":3500.0,"qty":0.20831598},{"id":"13500849898","px":3500.0,"qty":30.0},{"id":"13593438644","px":3490.0,"qty":0.03},{"id":"13500850443","px":3250.0,"qty":30.0},{"id":"13646060833","px":3000.0,"qty":0.1},{"id":"13500852289","px":3000.0,"qty":60.0},{"id":"13593444078","px":2990.0,"qty":0.03},{"id":"13468998724","px":2960.1,"qty":0.01839091},{"id":"13500872768","px":2750.0,"qty":30.0},{"id":"13464896579","px":2500.0,"qty":0.04742191},{"id":"13590103659","px":1250.0,"qty":0.07565798},{"id":"13614932851","px":1200.0,"qty":0.22399445},{"id":"13618805363","px":1200.0,"qty":5.66698318},{"id":"13604029252","px":1000.0,"qty":0.001},{"id":"13604031776","px":1000.0,"qty":0.001},{"id":"13604032926","px":1000.0,"qty":0.001},{"id":"13604066088","px":1000.0,"qty":0.001},{"id":"13604233355","px":1000.0,"qty":0.001},{"id":"13533381680","px":1000.0,"qty":2.58886178},{"id":"13640801973","px":989.0,"qty":0.00218992},{"id":"13507649679","px":875.0,"qty":0.02},{"id":"13507646803","px":500.0,"qty":0.2},{"id":"13633130795","px":201.0,"qty":2.95756139},{"id":"13600481737","px":117.0,"qty":2.0035},{"id":"13363888309","px":113.0,"qty":0.01133917},{"id":"13645983811","px":90.0,"qty":56.03086906},{"id":"13546483349","px":48.4,"qty":0.00660308},{"id":"13546501588","px":48.0,"qty":0.0065},{"id":"13458618144","px":15.3,"qty":0.00252606},{"id":"13608728917","px":15.0,"qty":0.00188792},{"id":"13522291774","px":9.5,"qty":0.00141542},{"id":"13504204853","px":6.6,"qty":9.8433E-4},{"id":"13426400352","px":6.0,"qty":6.0062E-4},{"id":"13592124243","px":6.0,"qty":9.7573E-4},{"id":"13541733268","px":5.0,"qty":5.0656E-4},{"id":"13614944944","px":4.4,"qty":4.5},{"id":"13614877652","px":4.4,"qty":6.06199279},{"id":"13490481486","px":1.0,"qty":600.0},{"id":"13622138397","px":0.2,"qty":1.0}],"asks":[{"id":"13649430164","px":8497.7,"qty":0.124},{"id":"13649430106","px":8500.7,"qty":0.618},{"id":"13649430188","px":8502.2,"qty":1.01},{"id":"13649430126","px":8503.5,"qty":9.3},{"id":"13649430170","px":8504.7,"qty":2.01},{"id":"13649430181","px":8504.9,"qty":1.0},{"id":"13649430171","px":8506.5,"qty":26.8},{"id":"13649430128","px":8506.5,"qty":36.0},{"id":"13649430100","px":8507.0,"qty":19.6},{"id":"13649430063","px":8507.2,"qty":3.01},{"id":"13649430130","px":8507.5,"qty":49.31},{"id":"13649429660","px":8508.0,"qty":5.0},{"id":"13649429998","px":8508.9,"qty":1.7649},{"id":"13649430133","px":8511.5,"qty":49.22},{"id":"13649430089","px":8513.8,"qty":3.5303},{"id":"13649430054","px":8515.8,"qty":2.02},{"id":"13649429452","px":8518.3,"qty":3.5284},{"id":"13649391121","px":8545.0,"qty":0.00244816},{"id":"13649430070","px":8566.7,"qty":5.8312063},{"id":"13649430055","px":8566.8,"qty":2.26},{"id":"13649071832","px":8586.0,"qty":0.01},{"id":"13649430098","px":8616.1,"qty":1.78},{"id":"13648514720","px":8750.0,"qty":0.0024823},{"id":"13648692649","px":8750.0,"qty":0.04716569},{"id":"13648044645","px":8825.0,"qty":0.03358068},{"id":"13647989559","px":8844.6,"qty":0.02},{"id":"13647745377","px":8860.0,"qty":0.015},{"id":"13647842155","px":8867.0,"qty":9.99E-4},{"id":"13648374935","px":8875.0,"qty":5.0E-4},{"id":"13648494500","px":8900.0,"qty":0.00137023},{"id":"13649374814","px":8900.0,"qty":0.00461822},{"id":"13647617210","px":8950.0,"qty":0.00236237},{"id":"13648246803","px":8950.0,"qty":0.00567081},{"id":"13648076843","px":8956.0,"qty":0.01},{"id":"13646172086","px":9000.0,"qty":0.001},{"id":"13646395055","px":9000.0,"qty":0.04550088},{"id":"13648015452","px":9000.0,"qty":0.2},{"id":"13649232867","px":9083.9,"qty":0.0032759},{"id":"13646177669","px":9100.0,"qty":5.1E-4},{"id":"13647676515","px":9100.0,"qty":8.7138E-4},{"id":"13649341529","px":9150.0,"qty":0.00164242},{"id":"13649232908","px":9171.2,"qty":0.00327591},{"id":"13648236709","px":9186.0,"qty":0.01},{"id":"13646180857","px":9200.0,"qty":5.1E-4},{"id":"13647677576","px":9200.0,"qty":7.0E-4},{"id":"13648701419","px":9200.0,"qty":0.005},{"id":"13647562273","px":9200.0,"qty":0.07327726},{"id":"13649232941","px":9302.1,"qty":0.00327593},{"id":"13648448160","px":9453.0,"qty":0.02},{"id":"13649233013","px":9476.9,"qty":0.00327592},{"id":"13648822858","px":9490.0,"qty":0.17121609},{"id":"13647201076","px":9490.0,"qty":0.2},{"id":"13647339212","px":9500.0,"qty":7.7488E-4},{"id":"13647175318","px":9502.2,"qty":0.015},{"id":"13647472462","px":9530.0,"qty":0.00550087},{"id":"13648627790","px":9545.0,"qty":0.09462243},{"id":"13645838807","px":9598.0,"qty":5.8E-4},{"id":"13647176999","px":9598.1,"qty":0.015},{"id":"13645868184","px":9600.0,"qty":5.1E-4},{"id":"13647400534","px":9600.0,"qty":0.001},{"id":"13648702172","px":9600.0,"qty":0.001},{"id":"13647085040","px":9600.0,"qty":0.00154235},{"id":"13647619440","px":9600.0,"qty":0.03708079},{"id":"13647179506","px":9624.1,"qty":0.015},{"id":"13645831255","px":9655.0,"qty":5.1E-4},{"id":"13647182506","px":9688.5,"qty":0.015},{"id":"13647083684","px":9700.0,"qty":0.001},{"id":"13648527484","px":9700.0,"qty":0.04209463},{"id":"13647186100","px":9724.2,"qty":0.015},{"id":"13647679107","px":9750.0,"qty":0.1},{"id":"13645815241","px":9755.0,"qty":5.1E-4},{"id":"13647190052","px":9788.8,"qty":0.015},{"id":"13647079327","px":9800.0,"qty":0.001},{"id":"13648321256","px":9800.0,"qty":0.4},{"id":"13647193821","px":9812.4,"qty":0.01},{"id":"13643382647","px":9818.0,"qty":5.0E-4},{"id":"13644149212","px":9850.0,"qty":0.001},{"id":"13648015928","px":9850.0,"qty":0.40579178},{"id":"13647195742","px":9854.1,"qty":0.01},{"id":"13642950792","px":9880.0,"qty":0.0071502},{"id":"13643045340","px":9885.0,"qty":0.01},{"id":"13648454467","px":9893.0,"qty":0.04},{"id":"13645057426","px":9899.0,"qty":0.26176124},{"id":"13643158883","px":9899.5,"qty":0.01},{"id":"13647081105","px":9900.0,"qty":0.001},{"id":"13646898715","px":9900.0,"qty":0.00672828},{"id":"13645498774","px":9900.0,"qty":0.00721689},{"id":"13645399638","px":9900.0,"qty":0.01974567},{"id":"13647861498","px":9950.0,"qty":0.01554376},{"id":"13643160123","px":9959.7,"qty":0.01},{"id":"13642584192","px":9975.0,"qty":0.001},{"id":"13644151608","px":9990.0,"qty":0.001},{"id":"13644164207","px":9990.0,"qty":0.99692503},{"id":"13643161554","px":9993.1,"qty":0.01},{"id":"13642397814","px":9994.0,"qty":0.01467174},{"id":"13644634510","px":9999.0,"qty":0.00960447},{"id":"13647078448","px":10000.0,"qty":0.001},{"id":"13647420352","px":10000.0,"qty":0.001002},{"id":"13643529731","px":10000.0,"qty":0.00514428},{"id":"13642275172","px":10000.0,"qty":0.00815906},{"id":"13647060134","px":10000.0,"qty":0.00989801},{"id":"13643992111","px":10000.0,"qty":0.01097054},{"id":"13644623244","px":10000.0,"qty":0.01217751},{"id":"13647204628","px":10000.0,"qty":0.01922903},{"id":"13648412995","px":10000.0,"qty":0.05},{"id":"13645435636","px":10000.0,"qty":0.18638632},{"id":"13644391051","px":10003.0,"qty":0.08100746},{"id":"13643162066","px":10023.4,"qty":0.01},{"id":"13641685530","px":10025.0,"qty":0.01629675},{"id":"13642781183","px":10036.0,"qty":0.0307},{"id":"13644636759","px":10050.0,"qty":0.00168038},{"id":"13643162162","px":10050.0,"qty":0.00505412},{"id":"13641482375","px":10050.0,"qty":0.05567946},{"id":"13644716848","px":10052.5,"qty":7.702E-4},{"id":"13641456806","px":10060.0,"qty":0.0150765},{"id":"13637417476","px":10065.0,"qty":0.65157008},{"id":"13643162669","px":10068.8,"qty":0.01},{"id":"13641510766","px":10100.0,"qty":0.005},{"id":"13649092243","px":10100.0,"qty":0.00571473},{"id":"13641637317","px":10100.0,"qty":0.25},{"id":"13648457737","px":10109.0,"qty":0.01},{"id":"13643163551","px":10125.2,"qty":0.01},{"id":"13643164301","px":10189.5,"qty":0.01},{"id":"13611260642","px":10200.0,"qty":9.0E-4},{"id":"13646696620","px":10200.0,"qty":0.00772834},{"id":"13481888846","px":10200.0,"qty":0.01346045},{"id":"13643165177","px":10229.3,"qty":0.01},{"id":"13394733514","px":10231.4,"qty":0.00123857},{"id":"13342776891","px":10250.0,"qty":0.001},{"id":"13342961845","px":10289.0,"qty":0.46046664},{"id":"13643165692","px":10289.3,"qty":0.01},{"id":"13649113446","px":10325.0,"qty":0.04},{"id":"13643166165","px":10326.2,"qty":0.01},{"id":"13639957523","px":10333.0,"qty":0.317},{"id":"13620381683","px":10360.0,"qty":0.11735025},{"id":"13643166917","px":10389.5,"qty":0.01},{"id":"13611261697","px":10400.0,"qty":8.6797E-4},{"id":"13642030230","px":10400.0,"qty":0.0032},{"id":"13321509853","px":10400.0,"qty":0.01426483},{"id":"13637739333","px":10400.0,"qty":0.046},{"id":"13644831024","px":10420.0,"qty":0.02},{"id":"13329528646","px":10500.0,"qty":5.3027E-4},{"id":"13628129988","px":10500.0,"qty":9.5339E-4},{"id":"13640005591","px":10500.0,"qty":0.001},{"id":"13638452688","px":10500.0,"qty":0.002},{"id":"13377704647","px":10500.0,"qty":0.00294235},{"id":"13642040568","px":10507.0,"qty":0.00796566},{"id":"13640742374","px":10539.7,"qty":0.02527625},{"id":"13649318213","px":10550.0,"qty":0.002},{"id":"13640401380","px":10564.0,"qty":0.005},{"id":"13633938415","px":10600.0,"qty":0.0015},{"id":"13305449913","px":10624.0,"qty":0.005},{"id":"13641679268","px":10745.0,"qty":1.0},{"id":"13649119345","px":10785.0,"qty":0.02},{"id":"13633938657","px":10800.0,"qty":0.0015},{"id":"13616338849","px":10800.0,"qty":0.00213942},{"id":"13647876268","px":10800.0,"qty":0.01554376},{"id":"13641333258","px":10800.0,"qty":0.14695779},{"id":"13611636110","px":10885.0,"qty":0.06},{"id":"13640404299","px":10989.0,"qty":0.005},{"id":"13641809665","px":10990.0,"qty":0.4},{"id":"13620495906","px":10993.0,"qty":0.015},{"id":"13644830906","px":10993.0,"qty":0.02},{"id":"13338367764","px":11000.0,"qty":0.001},{"id":"13633938836","px":11000.0,"qty":0.0015},{"id":"13642024291","px":11000.0,"qty":0.00211743},{"id":"13620907614","px":11000.0,"qty":0.02270304},{"id":"13640047895","px":11000.0,"qty":0.5},{"id":"13641088751","px":11111.0,"qty":5.0E-4},{"id":"13633941570","px":11200.0,"qty":0.001},{"id":"13641379813","px":11233.0,"qty":0.0026442},{"id":"13649123038","px":11302.0,"qty":0.01},{"id":"13640418502","px":11364.0,"qty":0.005},{"id":"13633941780","px":11400.0,"qty":0.00114808},{"id":"13644833877","px":11420.0,"qty":0.01332208},{"id":"13647877737","px":11500.0,"qty":0.01554377},{"id":"13648423087","px":11500.0,"qty":0.1130985},{"id":"13638605712","px":11600.0,"qty":0.002},{"id":"13611641484","px":11786.0,"qty":0.06},{"id":"13612848529","px":11800.0,"qty":5.996E-4},{"id":"13640431858","px":11844.0,"qty":0.01},{"id":"13648456986","px":11893.0,"qty":0.01},{"id":"13633631016","px":12000.0,"qty":0.00152098},{"id":"13644112470","px":12000.0,"qty":0.0223377},{"id":"13296028985","px":12000.0,"qty":0.82718574},{"id":"13641088981","px":12222.0,"qty":5.0E-4},{"id":"13644389433","px":12246.0,"qty":0.08174803},{"id":"13640435583","px":12300.0,"qty":0.01},{"id":"13641681040","px":12300.0,"qty":1.0},{"id":"13618224414","px":12500.0,"qty":0.00130199},{"id":"13641089835","px":13333.0,"qty":5.0E-4},{"id":"13485538651","px":13420.0,"qty":0.02},{"id":"13629859688","px":13498.0,"qty":0.5},{"id":"13472223304","px":14000.0,"qty":0.01},{"id":"13641089974","px":14444.0,"qty":5.0E-4},{"id":"13649126572","px":15000.0,"qty":0.06},{"id":"13629860573","px":15525.0,"qty":0.50095482},{"id":"13641090071","px":15555.0,"qty":5.0E-4},{"id":"13649233099","px":16110.6,"qty":0.00327592},{"id":"13641090355","px":16666.0,"qty":5.0E-4},{"id":"13497666623","px":17495.8,"qty":0.00232965},{"id":"13641090601","px":17777.0,"qty":5.0E-4},{"id":"13641090970","px":18888.0,"qty":5.0E-4},{"id":"13648071258","px":19000.0,"qty":0.01618178},{"id":"13640248287","px":19359.7,"qty":0.0130365},{"id":"13641091134","px":19999.0,"qty":5.0E-4},{"id":"13639734898","px":20000.0,"qty":0.07212326},{"id":"13641091477","px":21111.0,"qty":5.0E-4},{"id":"13497669023","px":21860.9,"qty":0.1},{"id":"13641091640","px":22222.0,"qty":5.0E-4},{"id":"13497669571","px":23112.0,"qty":7.2965E-4},{"id":"13641091852","px":23333.0,"qty":5.0E-4},{"id":"13641092091","px":24444.0,"qty":5.0E-4},{"id":"13497670145","px":25550.0,"qty":0.00116427},{"id":"13641092325","px":25555.0,"qty":5.0E-4},{"id":"13641092664","px":26666.0,"qty":5.0E-4},{"id":"13497671258","px":27008.0,"qty":9.2965E-4},{"id":"13641093355","px":27777.0,"qty":5.0E-4},{"id":"13641093783","px":28888.0,"qty":5.0E-4},{"id":"13497671795","px":29673.7,"qty":0.010005},{"id":"13641094298","px":29999.0,"qty":5.0E-4},{"id":"13637087085","px":30000.0,"qty":0.83727024},{"id":"13497672402","px":30003.0,"qty":6.2965E-4},{"id":"13641095568","px":31111.0,"qty":5.0E-4},{"id":"13497673459","px":31653.7,"qty":5.0001E-4},{"id":"13497674515","px":32222.3,"qty":0.00211112},{"id":"13497675303","px":33953.6,"qty":0.00147337},{"id":"13497676068","px":35000.7,"qty":0.00146498},{"id":"13628561602","px":50000.0,"qty":0.33270952},{"id":"13508526538","px":64733.0,"qty":0.01229168},{"id":"13620327509","px":200000.0,"qty":0.00540601},{"id":"13645924624","px":954200.0,"qty":6.0279E-4},{"id":"13643921825","px":964200.0,"qty":6.0E-4},{"id":"13643917367","px":969700.0,"qty":5.9839E-4}]}
    INFO:root:{"seqnum":103,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8491.8,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":104,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430163","px":8491.8,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":105,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8497.7,"qty":0.0}]}
    INFO:root:{"seqnum":106,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430164","px":8497.7,"qty":0.0}]}
    INFO:root:{"seqnum":107,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8492.3,"qty":0.124}],"asks":[]}
    INFO:root:{"seqnum":108,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430201","px":8492.3,"qty":0.124}],"asks":[]}
    INFO:root:{"seqnum":109,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8498.2,"qty":0.124}]}
    INFO:root:{"seqnum":110,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430209","px":8498.2,"qty":0.124}]}
    INFO:root:{"seqnum":111,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8493.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":112,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430189","px":8493.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":113,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8502.2,"qty":0.0}]}
    INFO:root:{"seqnum":114,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430188","px":8502.2,"qty":0.0}]}
    INFO:root:{"seqnum":115,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8492.6,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":116,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430211","px":8492.6,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":117,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8501.7,"qty":1.01}]}
    INFO:root:{"seqnum":118,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430212","px":8501.7,"qty":1.01}]}
    INFO:root:{"seqnum":119,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8501.7,"qty":0.0}]}
    INFO:root:{"seqnum":120,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430212","px":8501.7,"qty":0.0}]}
    INFO:root:{"seqnum":121,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8502.7,"qty":1.01}]}
    INFO:root:{"seqnum":122,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430218","px":8502.7,"qty":1.01}]}
    INFO:root:{"seqnum":123,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8492.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":124,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430211","px":8492.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":125,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8502.7,"qty":0.0}]}
    INFO:root:{"seqnum":126,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430218","px":8502.7,"qty":0.0}]}
    INFO:root:{"seqnum":127,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8493.1,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":128,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430219","px":8493.1,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":129,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8502.2,"qty":1.01}]}
    INFO:root:{"seqnum":130,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430220","px":8502.2,"qty":1.01}]}
    INFO:root:{"seqnum":131,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8502.2,"qty":0.0}]}
    INFO:root:{"seqnum":132,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430220","px":8502.2,"qty":0.0}]}
    INFO:root:{"seqnum":133,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8501.7,"qty":1.01}]}
    INFO:root:{"seqnum":134,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430221","px":8501.7,"qty":1.01}]}
    INFO:root:{"seqnum":135,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8501.7,"qty":0.0}]}
    INFO:root:{"seqnum":136,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430221","px":8501.7,"qty":0.0}]}
    INFO:root:{"seqnum":137,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8502.7,"qty":1.01}]}
    INFO:root:{"seqnum":138,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430222","px":8502.7,"qty":1.01}]}
    INFO:root:{"seqnum":139,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8491.4,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":140,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430180","px":8491.4,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":141,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.7,"qty":1.0}],"asks":[]}
    INFO:root:{"seqnum":142,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430229","px":8491.7,"qty":1.0}],"asks":[]}
    INFO:root:{"seqnum":143,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8502.7,"qty":0.0}]}
    INFO:root:{"seqnum":144,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430222","px":8502.7,"qty":0.0}]}
    INFO:root:{"seqnum":145,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8502.2,"qty":1.01}]}
    INFO:root:{"seqnum":146,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430231","px":8502.2,"qty":1.01}]}
    INFO:root:{"seqnum":147,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8493.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":148,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430219","px":8493.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":149,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8502.2,"qty":0.0}]}
    INFO:root:{"seqnum":150,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430231","px":8502.2,"qty":0.0}]}
    INFO:root:{"seqnum":151,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8492.6,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":152,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430238","px":8492.6,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":153,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8501.7,"qty":1.01}]}
    INFO:root:{"seqnum":154,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430239","px":8501.7,"qty":1.01}]}
    INFO:root:{"seqnum":155,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8511.5,"qty":0.0}]}
    INFO:root:{"seqnum":156,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430133","px":8511.5,"qty":0.0}]}
    INFO:root:{"seqnum":157,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8514.0,"qty":49.22}]}
    INFO:root:{"seqnum":158,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430240","px":8514.0,"qty":49.22}]}
    INFO:root:{"seqnum":159,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8501.7,"qty":0.0}]}
    INFO:root:{"seqnum":160,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430239","px":8501.7,"qty":0.0}]}
    INFO:root:{"seqnum":161,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8502.7,"qty":1.01}]}
    INFO:root:{"seqnum":162,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430244","px":8502.7,"qty":1.01}]}
    INFO:root:{"seqnum":163,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8492.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":164,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430238","px":8492.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":165,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8502.7,"qty":0.0}]}
    INFO:root:{"seqnum":166,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430244","px":8502.7,"qty":0.0}]}
    INFO:root:{"seqnum":167,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8507.2,"qty":0.0}]}
    INFO:root:{"seqnum":168,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430063","px":8507.2,"qty":0.0}]}
    INFO:root:{"seqnum":169,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.6,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":170,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430259","px":8491.6,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":171,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8501.7,"qty":1.01}]}
    INFO:root:{"seqnum":172,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430260","px":8501.7,"qty":1.01}]}
    INFO:root:{"seqnum":173,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":2,"px":8504.7,"qty":5.02}]}
    INFO:root:{"seqnum":174,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430261","px":8504.7,"qty":3.01}]}
    INFO:root:{"seqnum":175,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8491.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":176,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430259","px":8491.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":177,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8501.7,"qty":0.0}]}
    INFO:root:{"seqnum":178,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430260","px":8501.7,"qty":0.0}]}
    INFO:root:{"seqnum":179,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8504.7,"qty":3.01}]}
    INFO:root:{"seqnum":180,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430170","px":8504.7,"qty":0.0}]}
    INFO:root:{"seqnum":181,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.1,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":182,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430267","px":8491.1,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":183,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8500.2,"qty":1.01}]}
    INFO:root:{"seqnum":184,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430268","px":8500.2,"qty":1.01}]}
    INFO:root:{"seqnum":185,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8502.2,"qty":2.01}]}
    INFO:root:{"seqnum":186,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430269","px":8502.2,"qty":2.01}]}
    INFO:root:{"seqnum":187,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8491.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":188,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430267","px":8491.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":189,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8500.2,"qty":0.0}]}
    INFO:root:{"seqnum":190,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430268","px":8500.2,"qty":0.0}]}
    INFO:root:{"seqnum":191,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":2,"px":8490.6,"qty":1.628}],"asks":[]}
    INFO:root:{"seqnum":192,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430279","px":8490.6,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":193,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8499.7,"qty":1.01}]}
    INFO:root:{"seqnum":194,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430280","px":8499.7,"qty":1.01}]}
    INFO:root:{"seqnum":195,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8504.9,"qty":0.0}]}
    INFO:root:{"seqnum":196,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430181","px":8504.9,"qty":0.0}]}
    INFO:root:{"seqnum":197,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8506.0,"qty":1.0}]}
    INFO:root:{"seqnum":198,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430285","px":8506.0,"qty":1.0}]}
    INFO:root:{"seqnum":199,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8499.7,"qty":0.0}]}
    INFO:root:{"seqnum":200,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430280","px":8499.7,"qty":0.0}]}
    INFO:root:{"seqnum":201,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8502.2,"qty":0.0}]}
    INFO:root:{"seqnum":202,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430269","px":8502.2,"qty":0.0}]}
    INFO:root:{"seqnum":203,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8504.7,"qty":0.0}]}
    INFO:root:{"seqnum":204,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430261","px":8504.7,"qty":0.0}]}
    INFO:root:{"seqnum":205,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8504.2,"qty":1.01}]}
    INFO:root:{"seqnum":206,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430287","px":8504.2,"qty":1.01}]}
    INFO:root:{"seqnum":207,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8506.2,"qty":2.01}]}
    INFO:root:{"seqnum":208,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430288","px":8506.2,"qty":2.01}]}
    INFO:root:{"seqnum":209,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8509.2,"qty":3.01}]}
    INFO:root:{"seqnum":210,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430289","px":8509.2,"qty":3.01}]}
    [HeartbeatChannel(is_subscribed=True),
     OrderbookL2Channel(symbol=BTC-USD, is_subscribed=True),
     OrderbookL3Channel(symbol=BTC-USD, is_subscribed=True),
     PricesChannel(symbol=BTC-USD, granularity=60, is_subscribed=True),
     PricesChannel(symbol=ETH-USD, granularity=60, is_subscribed=True),
     SymbolsChannel(is_subscribed=True),
     TickerChannel(symbol=BTC-USD, is_subscribed=True),
     TradesChannel(symbol=BTC-USD, is_subscribed=True)]
    INFO:root:{"seqnum":211,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8490.6,"qty":0.618}],"asks":[]}
    INFO:root:{"seqnum":212,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430279","px":8490.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":213,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8504.2,"qty":0.0}]}
    INFO:root:{"seqnum":214,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430287","px":8504.2,"qty":0.0}]}
    INFO:root:{"seqnum":215,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8506.2,"qty":0.0}]}
    INFO:root:{"seqnum":216,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430288","px":8506.2,"qty":0.0}]}
    INFO:root:{"seqnum":217,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8509.2,"qty":0.0}]}
    INFO:root:{"seqnum":218,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430289","px":8509.2,"qty":0.0}]}
    INFO:root:{"seqnum":219,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8492.6,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":220,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430296","px":8492.6,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":221,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8501.7,"qty":1.01}]}
    INFO:root:{"seqnum":222,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430297","px":8501.7,"qty":1.01}]}
    INFO:root:{"seqnum":223,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8504.2,"qty":2.01}]}
    INFO:root:{"seqnum":224,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430298","px":8504.2,"qty":2.01}]}
    INFO:root:{"seqnum":225,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8507.2,"qty":3.01}]}
    INFO:root:{"seqnum":226,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430299","px":8507.2,"qty":3.01}]}
    INFO:root:{"seqnum":227,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8501.7,"qty":0.0}]}
    INFO:root:{"seqnum":228,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430297","px":8501.7,"qty":0.0}]}
    INFO:root:{"seqnum":229,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8502.7,"qty":1.01}]}
    INFO:root:{"seqnum":230,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430306","px":8502.7,"qty":1.01}]}
    INFO:root:{"seqnum":231,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8492.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":232,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430296","px":8492.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":233,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8502.7,"qty":0.0}]}
    INFO:root:{"seqnum":234,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430306","px":8502.7,"qty":0.0}]}
    INFO:root:{"seqnum":235,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8493.1,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":236,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430312","px":8493.1,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":237,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8502.2,"qty":1.01}]}
    INFO:root:{"seqnum":238,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430313","px":8502.2,"qty":1.01}]}
    INFO:root:{"seqnum":239,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8492.3,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":240,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430201","px":8492.3,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":241,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8498.2,"qty":0.0}]}
    INFO:root:{"seqnum":242,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430209","px":8498.2,"qty":0.0}]}
    INFO:root:{"seqnum":243,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8493.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":244,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430312","px":8493.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":245,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8502.2,"qty":0.0}]}
    INFO:root:{"seqnum":246,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430313","px":8502.2,"qty":0.0}]}
    INFO:root:{"seqnum":247,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8492.6,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":248,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430317","px":8492.6,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":249,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8502.7,"qty":1.01}]}
    INFO:root:{"seqnum":250,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430318","px":8502.7,"qty":1.01}]}
    INFO:root:{"seqnum":251,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8492.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":252,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430317","px":8492.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":253,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8502.7,"qty":0.0}]}
    INFO:root:{"seqnum":254,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430318","px":8502.7,"qty":0.0}]}
    INFO:root:{"seqnum":255,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8493.1,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":256,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430320","px":8493.1,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":257,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8501.7,"qty":1.01}]}
    INFO:root:{"seqnum":258,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430321","px":8501.7,"qty":1.01}]}
    INFO:root:{"seqnum":259,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8506.0,"qty":0.0}]}
    INFO:root:{"seqnum":260,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430285","px":8506.0,"qty":0.0}]}
    INFO:root:{"seqnum":261,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8505.8,"qty":1.0}]}
    INFO:root:{"seqnum":262,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430325","px":8505.8,"qty":1.0}]}
    INFO:root:{"seqnum":263,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8501.7,"qty":0.0}]}
    INFO:root:{"seqnum":264,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430321","px":8501.7,"qty":0.0}]}
    INFO:root:{"seqnum":265,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8502.2,"qty":1.01}]}
    INFO:root:{"seqnum":266,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430326","px":8502.2,"qty":1.01}]}
    INFO:root:{"seqnum":267,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8492.2,"qty":0.124}],"asks":[]}
    INFO:root:{"seqnum":268,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430336","px":8492.2,"qty":0.124}],"asks":[]}
    INFO:root:{"seqnum":269,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8498.1,"qty":0.124}]}
    INFO:root:{"seqnum":270,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430337","px":8498.1,"qty":0.124}]}
    INFO:root:{"seqnum":271,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8493.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":272,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430320","px":8493.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":273,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8502.2,"qty":0.0}]}
    INFO:root:{"seqnum":274,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430326","px":8502.2,"qty":0.0}]}
    INFO:root:{"seqnum":275,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8507.2,"qty":0.0}]}
    INFO:root:{"seqnum":276,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430299","px":8507.2,"qty":0.0}]}
    INFO:root:{"seqnum":277,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.6,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":278,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430342","px":8491.6,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":279,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8501.7,"qty":1.01}]}
    INFO:root:{"seqnum":280,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430343","px":8501.7,"qty":1.01}]}
    INFO:root:{"seqnum":281,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8505.2,"qty":3.01}]}
    INFO:root:{"seqnum":282,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430344","px":8505.2,"qty":3.01}]}
    INFO:root:{"seqnum":283,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8501.7,"qty":0.0}]}
    INFO:root:{"seqnum":284,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430343","px":8501.7,"qty":0.0}]}
    INFO:root:{"seqnum":285,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8505.2,"qty":0.0}]}
    INFO:root:{"seqnum":286,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430344","px":8505.2,"qty":0.0}]}
    INFO:root:{"seqnum":287,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8503.7,"qty":1.01}]}
    INFO:root:{"seqnum":288,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430345","px":8503.7,"qty":1.01}]}
    INFO:root:{"seqnum":289,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8506.7,"qty":3.01}]}
    INFO:root:{"seqnum":290,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430348","px":8506.7,"qty":3.01}]}
    INFO:root:{"seqnum":291,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8491.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":292,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430342","px":8491.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":293,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8503.7,"qty":0.0}]}
    INFO:root:{"seqnum":294,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430345","px":8503.7,"qty":0.0}]}
    INFO:root:{"seqnum":295,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.1,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":296,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430351","px":8491.1,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":297,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8501.2,"qty":1.01}]}
    INFO:root:{"seqnum":298,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430352","px":8501.2,"qty":1.01}]}
    INFO:root:{"seqnum":299,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8501.2,"qty":0.0}]}
    INFO:root:{"seqnum":300,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430352","px":8501.2,"qty":0.0}]}
    INFO:root:{"seqnum":301,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8504.2,"qty":0.0}]}
    INFO:root:{"seqnum":302,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430298","px":8504.2,"qty":0.0}]}
    INFO:root:{"seqnum":303,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8500.2,"qty":1.01}]}
    INFO:root:{"seqnum":304,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430354","px":8500.2,"qty":1.01}]}
    INFO:root:{"seqnum":305,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8502.2,"qty":2.01}]}
    INFO:root:{"seqnum":306,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430355","px":8502.2,"qty":2.01}]}
    INFO:root:{"seqnum":307,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8500.2,"qty":0.0}]}
    INFO:root:{"seqnum":308,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430354","px":8500.2,"qty":0.0}]}
    INFO:root:{"seqnum":309,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8499.7,"qty":1.01}]}
    INFO:root:{"seqnum":310,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430356","px":8499.7,"qty":1.01}]}
    INFO:root:{"seqnum":311,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8506.5,"qty":36.0}]}
    INFO:root:{"seqnum":312,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430171","px":8506.5,"qty":0.0}]}
    INFO:root:{"seqnum":313,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8505.0,"qty":26.8}]}
    INFO:root:{"seqnum":314,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430358","px":8505.0,"qty":26.8}]}
    INFO:root:{"seqnum":315,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8505.8,"qty":0.0}]}
    INFO:root:{"seqnum":316,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430325","px":8505.8,"qty":0.0}]}
    INFO:root:{"seqnum":317,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8506.0,"qty":1.0}]}
    INFO:root:{"seqnum":318,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430360","px":8506.0,"qty":1.0}]}
    INFO:root:{"seqnum":319,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8499.7,"qty":0.0}]}
    INFO:root:{"seqnum":320,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430356","px":8499.7,"qty":0.0}]}
    INFO:root:{"seqnum":321,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8502.2,"qty":0.0}]}
    INFO:root:{"seqnum":322,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430355","px":8502.2,"qty":0.0}]}
    INFO:root:{"seqnum":323,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8503.7,"qty":1.01}]}
    INFO:root:{"seqnum":324,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430361","px":8503.7,"qty":1.01}]}
    INFO:root:{"seqnum":325,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8505.2,"qty":2.01}]}
    INFO:root:{"seqnum":326,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430362","px":8505.2,"qty":2.01}]}
    INFO:root:{"seqnum":327,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8491.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":328,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430351","px":8491.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":329,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8503.7,"qty":0.0}]}
    INFO:root:{"seqnum":330,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430361","px":8503.7,"qty":0.0}]}
    INFO:root:{"seqnum":331,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8505.2,"qty":0.0}]}
    INFO:root:{"seqnum":332,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430362","px":8505.2,"qty":0.0}]}
    INFO:root:{"seqnum":333,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8492.1,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":334,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430363","px":8492.1,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":335,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":2,"px":8500.7,"qty":1.628}]}
    INFO:root:{"seqnum":336,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430364","px":8500.7,"qty":1.01}]}
    INFO:root:{"seqnum":337,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8503.7,"qty":2.01}]}
    INFO:root:{"seqnum":338,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430365","px":8503.7,"qty":2.01}]}
    INFO:root:{"seqnum":339,"event":"updated","channel":"heartbeat","timestamp":"2020-05-10T18:33:50.873910Z"}
    INFO:root:{"seqnum":340,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8492.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":341,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430363","px":8492.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":342,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.1,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":343,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430367","px":8491.1,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":344,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8500.7,"qty":0.618}]}
    INFO:root:{"seqnum":345,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430364","px":8500.7,"qty":0.0}]}
    INFO:root:{"seqnum":346,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8503.7,"qty":0.0}]}
    INFO:root:{"seqnum":347,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430365","px":8503.7,"qty":0.0}]}
    INFO:root:{"seqnum":348,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8499.7,"qty":1.01}]}
    INFO:root:{"seqnum":349,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430368","px":8499.7,"qty":1.01}]}
    INFO:root:{"seqnum":350,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8501.7,"qty":2.01}]}
    INFO:root:{"seqnum":351,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430369","px":8501.7,"qty":2.01}]}
    INFO:root:{"seqnum":352,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8492.2,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":353,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430336","px":8492.2,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":354,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8498.1,"qty":0.0}]}
    INFO:root:{"seqnum":355,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430337","px":8498.1,"qty":0.0}]}
    INFO:root:{"seqnum":356,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":2,"px":8491.7,"qty":1.124}],"asks":[]}
    INFO:root:{"seqnum":357,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430373","px":8491.7,"qty":0.124}],"asks":[]}
    INFO:root:{"seqnum":358,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8497.6,"qty":0.124}]}
    INFO:root:{"seqnum":359,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430374","px":8497.6,"qty":0.124}]}
    INFO:root:{"seqnum":360,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.7,"qty":0.124}],"asks":[]}
    INFO:root:{"seqnum":361,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430229","px":8491.7,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":362,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.4,"qty":1.0}],"asks":[]}
    INFO:root:{"seqnum":363,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430380","px":8491.4,"qty":1.0}],"asks":[]}
    INFO:root:{"seqnum":364,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8491.4,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":365,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430380","px":8491.4,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":366,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8506.0,"qty":0.0}]}
    INFO:root:{"seqnum":367,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430360","px":8506.0,"qty":0.0}]}
    INFO:root:{"seqnum":368,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.6,"qty":1.0}],"asks":[]}
    INFO:root:{"seqnum":369,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430391","px":8491.6,"qty":1.0}],"asks":[]}
    INFO:root:{"seqnum":370,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8505.5,"qty":1.0}]}
    INFO:root:{"seqnum":371,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430392","px":8505.5,"qty":1.0}]}
    INFO:root:{"seqnum":372,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8490.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":373,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430102","px":8490.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":374,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8500.7,"qty":0.0}]}
    INFO:root:{"seqnum":375,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430106","px":8500.7,"qty":0.0}]}
    INFO:root:{"seqnum":376,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8506.7,"qty":0.0}]}
    INFO:root:{"seqnum":377,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430348","px":8506.7,"qty":0.0}]}
    INFO:root:{"seqnum":378,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8508.7,"qty":3.01}]}
    INFO:root:{"seqnum":379,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430394","px":8508.7,"qty":3.01}]}
    INFO:root:{"seqnum":380,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8490.1,"qty":0.618}],"asks":[]}
    INFO:root:{"seqnum":381,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430396","px":8490.1,"qty":0.618}],"asks":[]}
    INFO:root:{"seqnum":382,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8500.2,"qty":0.618}]}
    INFO:root:{"seqnum":383,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430397","px":8500.2,"qty":0.618}]}
    INFO:root:{"seqnum":384,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8505.5,"qty":0.0}]}
    INFO:root:{"seqnum":385,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430392","px":8505.5,"qty":0.0}]}
    INFO:root:{"seqnum":386,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8505.3,"qty":1.0}]}
    INFO:root:{"seqnum":387,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430411","px":8505.3,"qty":1.0}]}
    INFO:root:{"seqnum":388,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8491.7,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":389,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430373","px":8491.7,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":390,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8497.6,"qty":0.0}]}
    INFO:root:{"seqnum":391,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430374","px":8497.6,"qty":0.0}]}
    INFO:root:{"seqnum":392,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8508.7,"qty":0.0}]}
    INFO:root:{"seqnum":393,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430394","px":8508.7,"qty":0.0}]}
    INFO:root:{"seqnum":394,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8506.7,"qty":3.01}]}
    INFO:root:{"seqnum":395,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430414","px":8506.7,"qty":3.01}]}
    INFO:root:{"seqnum":396,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.5,"qty":0.124}],"asks":[]}
    INFO:root:{"seqnum":397,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430416","px":8491.5,"qty":0.124}],"asks":[]}
    INFO:root:{"seqnum":398,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8497.4,"qty":0.124}]}
    INFO:root:{"seqnum":399,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430417","px":8497.4,"qty":0.124}]}
    INFO:root:{"seqnum":400,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8506.7,"qty":0.0}]}
    INFO:root:{"seqnum":401,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430414","px":8506.7,"qty":0.0}]}
    INFO:root:{"seqnum":402,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8508.7,"qty":3.01}]}
    INFO:root:{"seqnum":403,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430424","px":8508.7,"qty":3.01}]}
    INFO:root:{"seqnum":404,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8491.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":405,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430391","px":8491.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":406,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8505.3,"qty":0.0}]}
    INFO:root:{"seqnum":407,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430411","px":8505.3,"qty":0.0}]}
    INFO:root:{"seqnum":408,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":2,"px":8489.4,"qty":10.8}],"asks":[]}
    INFO:root:{"seqnum":409,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430427","px":8489.4,"qty":1.0}],"asks":[]}
    INFO:root:{"seqnum":410,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":2,"px":8505.0,"qty":27.8}]}
    INFO:root:{"seqnum":411,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430428","px":8505.0,"qty":1.0}]}
    INFO:root:{"seqnum":412,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8491.5,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":413,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430416","px":8491.5,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":414,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8497.4,"qty":0.0}]}
    INFO:root:{"seqnum":415,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430417","px":8497.4,"qty":0.0}]}
    INFO:root:{"seqnum":416,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8488.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":417,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649429994","px":8488.6,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":418,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8508.7,"qty":0.0}]}
    INFO:root:{"seqnum":419,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430424","px":8508.7,"qty":0.0}]}
    INFO:root:{"seqnum":420,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8485.6,"qty":2.01}],"asks":[]}
    INFO:root:{"seqnum":421,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430433","px":8485.6,"qty":2.01}],"asks":[]}
    INFO:root:{"seqnum":422,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8506.2,"qty":3.01}]}
    INFO:root:{"seqnum":423,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430434","px":8506.2,"qty":3.01}]}
    INFO:root:{"seqnum":424,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.5,"qty":0.124}],"asks":[]}
    INFO:root:{"seqnum":425,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430435","px":8491.5,"qty":0.124}],"asks":[]}
    INFO:root:{"seqnum":426,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8497.4,"qty":0.124}]}
    INFO:root:{"seqnum":427,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430436","px":8497.4,"qty":0.124}]}
    INFO:root:{"seqnum":428,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8491.5,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":429,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430435","px":8491.5,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":430,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8497.4,"qty":0.0}]}
    INFO:root:{"seqnum":431,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430436","px":8497.4,"qty":0.0}]}
    INFO:root:{"seqnum":432,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8491.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":433,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430367","px":8491.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":434,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8490.6,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":435,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430439","px":8490.6,"qty":1.01}],"asks":[]}
    INFO:root:{"seqnum":436,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8491.0,"qty":0.124}],"asks":[]}
    INFO:root:{"seqnum":437,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430440","px":8491.0,"qty":0.124}],"asks":[]}
    INFO:root:{"seqnum":438,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8496.9,"qty":0.124}]}
    INFO:root:{"seqnum":439,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430441","px":8496.9,"qty":0.124}]}
    INFO:root:{"seqnum":440,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8499.7,"qty":0.0}]}
    INFO:root:{"seqnum":441,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430368","px":8499.7,"qty":0.0}]}
    INFO:root:{"seqnum":442,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8499.2,"qty":1.01}]}
    INFO:root:{"seqnum":443,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430448","px":8499.2,"qty":1.01}]}
    INFO:root:{"seqnum":444,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8505.0,"qty":26.8}]}
    INFO:root:{"seqnum":445,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430428","px":8505.0,"qty":0.0}]}
    INFO:root:{"seqnum":446,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8503.2,"qty":1.0}]}
    INFO:root:{"seqnum":447,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430450","px":8503.2,"qty":1.0}]}
    INFO:root:{"seqnum":448,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":0,"px":8508.9,"qty":0.0}]}
    INFO:root:{"seqnum":449,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649429998","px":8508.9,"qty":0.0}]}
    INFO:root:{"seqnum":450,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":0,"px":8489.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":451,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649428955","px":8489.1,"qty":0.0}],"asks":[]}
    INFO:root:{"seqnum":452,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[],"asks":[{"num":1,"px":8506.9,"qty":1.7653}]}
    INFO:root:{"seqnum":453,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[],"asks":[{"id":"13649430451","px":8506.9,"qty":1.7653}]}
    INFO:root:{"seqnum":454,"event":"updated","channel":"l2","symbol":"BTC-USD","bids":[{"num":1,"px":8482.1,"qty":3.5307}],"asks":[]}
    INFO:root:{"seqnum":455,"event":"updated","channel":"l3","symbol":"BTC-USD","bids":[{"id":"13649430452","px":8482.1,"qty":3.5307}],"asks":[]}
    Last Heart Beat: 2020-05-10 18:33:50.873910






|


.. code-block:: default

    import time
    import logging
    from pprint import pprint
    from blockchain_exchange.client import BlockchainWebsocketClient


    logging.basicConfig(level=logging.INFO)


    def main():
        client = BlockchainWebsocketClient()
        client.subscribe_to_heartbeat()
        client.subscribe_to_prices("BTC-USD", granularity=60)
        client.subscribe_to_prices("ETH-USD", granularity=60)
        client.subscribe_to_ticker("BTC-USD")
        client.subscribe_to_trades("BTC-USD")
        time.sleep(2)
        pprint(client.connected_channels)

        time.sleep(2)
        client.subscribe_to_symbols()
        time.sleep(2)
        pprint(client.connected_channels)

        time.sleep(2)
        client.subscribe_to_orderbook_l2("BTC-USD")
        time.sleep(2)
        pprint(client.connected_channels)

        time.sleep(2)
        client.subscribe_to_orderbook_l3("BTC-USD")
        time.sleep(2)
        pprint(client.connected_channels)

        time.sleep(7)
        print(f"Last Heart Beat: {client.get_last_heartbeat()}")


    if __name__ == '__main__':
        main()


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  21.224 seconds)


.. _sphx_glr_download_generated_sphinx_gallery_run-00-subscribe-to-public-channels.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: run-00-subscribe-to-public-channels.py <run-00-subscribe-to-public-channels.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: run-00-subscribe-to-public-channels.ipynb <run-00-subscribe-to-public-channels.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
