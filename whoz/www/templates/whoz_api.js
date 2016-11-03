
///////////////////////////
// Create an immediately invoked functional expression to wrap our code
(function() {

    // Define our constructor
    this.whoz = function() {

        // Create global element references
        this.results = null;


        // Define option defaults
        var defaults = {
            search_url: '{{g.URL_BASE}}/search',
            search_species: null,
            search_limit: 1000,
            search_exact: false,
            //jquery_url: '{{g.URL_BASE}}/js/jquery.js'
        }

        console.log(defaults);

        // Create options by extending defaults with the passed in arguments
        if (arguments[0] && typeof arguments[0] === "object") {
            this.options = extendDefaults(defaults, arguments[0]);
        } else {
            this.options = defaults;
        }

        console.log(this.options);

        // init anything else
        initialize.call(this);

    }

  // Public Methods

  whoz.prototype.search = function(term, options, callback) {
      var _ = this;
      var $ = window.$ || window.JQuery;
      _.results = null;

      var search_data = {
          term: term,
          species: _.options.search_species,
          limit: _.options.search_limit,
          exact: _.options.search_exact
      };

      console.log('search_data = ', search_data);

      if (options && typeof options === 'object') {
          search_data = extendDefaults(search_data, options);
      }

      console.log('search_data = ', search_data);

      $.ajax({
          url: _.options.search_url,
          dataType: "jsonp",
          jsonp: 'callback',
          data: search_data
      }).done(function (data, textStatus, jqXHR) {
          console.log('done');
          console.log('data', data);
          console.log('textStatus', textStatus);
          console.log('jqXHR', jqXHR);
          _.results = data.genes;

          if (callback) {
              callback(data.genes);
          }

      }).fail(function (jqXHR, textStatus, errorThrown) {
          console.log('fail');
          console.log('jqXHR', jqXHR);
          console.log('textStatus', textStatus);
          console.log('errorThrown', errorThrown);

      }).always(function (data_jqXHR, textStatus, jqXHR_errorThrown) {
          console.log('always');
          console.log('data_jqXHR', data_jqXHR);
          console.log('textStatus', textStatus);
          console.log('jqXHR_errorThrown', jqXHR_errorThrown);

      });
  }

  // Private Methods

  function extendDefaults(source, properties) {
    var property;
    for (property in properties) {
      if (properties.hasOwnProperty(property)) {
        source[property] = properties[property];
      }
    }
    return source;
  }

  function initialize() {
        //console.log('check_jquery');
        var jquery = window.$ || window.JQuery;
        if (jquery === undefined || jquery.fn.jquery !== '2.0.3') {
            loadfile(this.options.jquery_url, 'js');//, main);
            console.log('jquery: loaded');
        } else {
            //main();
        }

  }

  function loadfile(filesrc, filetype, onload) {
    if (filetype == "js") { //if filename is a external JavaScript file
        var fileref = document.createElement('script');
        fileref.setAttribute("type", "text/javascript");
        fileref.setAttribute("src", filesrc);
        fileref.setAttribute("async", true)
    }
    else if (filetype == "css") { //if filename is an external CSS file
        var fileref = document.createElement("link");
        fileref.setAttribute("rel", "stylesheet");
        fileref.setAttribute("type", "text/css");
        fileref.setAttribute("href", filesrc);
        fileref.setAttribute("async", true)
    }
    if (typeof fileref != "undefined")
        if (fileref.readyState) {
            fileref.onreadystatechange = function () { // For old versions of IE
                if (this.readyState == 'complete' || this.readyState == 'loaded') {
                    onload();
                }
            };
        } else {
            fileref.onload = onload;
        }

    (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(fileref)
}


//ref:http://www.tomhoppe.com/index.php/2008/03/dynamically-adding-css-through-javascript/
function add_css(cssCode) {
    var styleElement = document.createElement("style");
    styleElement.type = "text/css";
    if (styleElement.styleSheet) {
        styleElement.styleSheet.cssText = cssCode;
    } else {
        styleElement.appendChild(document.createTextNode(cssCode));
    }
    document.getElementsByTagName("head")[0].appendChild(styleElement);
}

}());

///////////////////////////
