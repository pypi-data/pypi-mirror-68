## Changelog

0.8.0 (2020-05-11)
------------------

* Make structlog optional.
  [am-on]

* Support setting event props from HTTP headers.
  [am-on]


0.7.0 (2019-12-19)
------------------

* Added support for `people_union()`.
  [am-on]

* Added `sayanarijit/typecov`.
  [sayanarijit]


0.6.0 (2019-08-26)
------------------

* Added support for configuring a custom Consumer.
  [zupo]


0.5.0 (2019-08-25)
------------------

* Require that all Consumers implement a `flush()` method.
  [zupo]


0.4.3 (2019-08-24)
------------------

* Include py.typed in the package, third time is the charm?
  [zupo]


0.4.2 (2019-08-24)
------------------

* Include py.typed in the package, now for real.
  [zupo]


0.4.1 (2019-08-24)
------------------

* Include py.typed in the package.
  [zupo]


0.4.0 (2019-08-19)
------------------

* Prepare for PYPI release of the rewrite.
  [zupo]

* Small performance optimization.
  [zupo]


0.3.0 (2019-08-09)
------------------

* Add guards that make sure parameters sent to MixpanelTrack are valid.
  [zupo]

* Don't flood logs with "mixpanel configured" messages.
  [zupo]

* Support for the `people_append` method.
  [suryasr007]

* Lots of cleanup of legacy assumptions:
  * `profile_sync` method was removed
  * request.user no longer required
  * MixpanelTrack init now accepts `distinct_id` instead of `user`
  * `state` ProfileProperty no longer required
  [zupo]


0.2.1 (2019-07-28)
------------------

* Not all consumers have a .flush() method.
  [zupo]


0.2.0 (2019-07-27)
------------------

* Rewrite based on 5 years of Mixpanel usage in production at Niteo.
  [@zupo, @vanclevstik, @dz0ny, @karantan, @am-on, @rokcarl]


0.1.14 - 0.1.65 (2012-2014)
---------------------------

* Legacy version developed by @hadrien.
