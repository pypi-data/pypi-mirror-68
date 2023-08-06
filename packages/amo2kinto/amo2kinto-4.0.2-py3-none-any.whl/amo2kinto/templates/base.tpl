<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Blocked Add-ons</title>

    <link rel="shortcut icon" type="image/x-icon"
          href="https://addons.cdn.mozilla.net/static/img/favicon.ico">


    <link href="https://addons.cdn.mozilla.net/static/css/tabzilla/tabzilla.css" rel="stylesheet" />
    <link rel="stylesheet" media="all" href="https://addons.cdn.mozilla.net/static/css/zamboni/css-min.css?build=252d406" />
    <!--[if IE]><link rel="stylesheet" href="https://addons.cdn.mozilla.net/static/css/legacy/ie.css"><![endif]-->
    <!--[if IE 7]><link rel="stylesheet" href="https://addons.cdn.mozilla.net/static/css/legacy/ie7.css"><![endif]-->

    <link rel="stylesheet" href="https://addons.cdn.mozilla.net/static/css/zamboni/blocklist.css">
    <link rel="stylesheet" media="all" href="https://addons.cdn.mozilla.net/static/css/restyle/css-min.css?build=dd224a5" />
    <noscript><link rel="stylesheet" href="https://addons.cdn.mozilla.net/static/css/legacy/nojs.css"></noscript>
    <script src="https://addons.cdn.mozilla.net/static/js/preload-min.js?build=d97d82ed-5b34d014"></script>
  </head>
  <body class="html-ltr firefox moz-header-slim restyle">
      <div id="main-wrapper">
          <div id="background-wrapper"></div>
          <div class="section">
              <div class="header-bg">
                  <div class="amo-header-wrapper">
                      <div id="tabzilla">
                          <a href="https://www.mozilla.org/">Mozilla</a>
                      </div>
                      <div class="amo-header">
                          <div id="masthead">
                              <h1 class="site-title">
                                  <a href="./" title="Back to add-ons list.">
                                      <img alt="" src="https://addons.cdn.mozilla.net/static/img/icons/firefox.png?b=d97d82ed-5b34d014">
                                      Blocked  Add-ons
                                  </a>
                              </h1>

                              <nav id="site-nav" class="menu-nav c">
                              </nav>
                          </div>
                      </div>
                  </div>
              </div>
              <ol id="breadcrumbs" class="breadcrumbs">
                  <li>Blocked Add-ons</li>
              </ol>
              {% block content %}{% endblock %}
              </div>
          </div>
      <div id="footer" role="contentinfo">
          <div class="section">
              <img class="footerlogo" src="https://addons.cdn.mozilla.net/static/img/zamboni/footer-logo-med.png" alt="Footer logo">
              <div class="links-footer">
                  <ul>
                      <li>get to know <b>add-ons</b></li>
                      <li><a href="https://addons.mozilla.org/en-US/about">About</a></li>
                      <li><a href="https://blog.mozilla.org/addons/">Blog</a></li>
                      <li class="footer-devhub-link"><a href="https://addons.mozilla.org/en-US/developers/">Developer Hub</a></li>
                      <li><a href="https://discourse.mozilla.org/c/add-ons">Forum</a></li>
                  </ul>
              </div>
              <div id="footer-content">
                  <div id="copyright">
                      <p id="footer-links">
                          <a href="http://www.mozilla.org/privacy/websites/">
                              Privacy Policy
                          </a> &nbsp;|&nbsp;
                          <a href="https://www.mozilla.org/about/legal/">
                              Legal Notices
                          </a> &nbsp;|&nbsp;
                          <a href="https://www.mozilla.org/about/legal/fraud-report/">
                              Report Trademark Abuse
                          </a>
                          &nbsp;|&nbsp;<a href="https://status.mozilla.org/">Site Status</a>
                      </p>
                      <p>
                          Except where otherwise <a href="https://www.mozilla.org/about/legal/">noted</a>, content on this site is licensed under the <br /> <a href="https://creativecommons.org/licenses/by-sa/3.0/"> Creative Commons Attribution Share-Alike License v3.0 </a> or any later version.</p>
                  </div>
              </div>
          </div>
      </div>
  </body>
</html>
