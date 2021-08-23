var fuse_dispdlts;
var fuse_shipdlts;


function dispdlts_result_to_domstr(result) {
    var domstr = "<div class='dispdlts-search-result' data-dispdlts='" + JSON.stringify(result) + "'>"+
    "<div>"+ result['dispdlts_name'] + "</div>" +
    "<div>"+ result['dispdlts_address1'] + "</div>" +
    "<div>"+ result['dispdlts_address2'] + "</div>" +
    "<div>"+ result['dispdlts_loc'] + "</div>" +
    "<div>"+ result['dispdlts_pin'] + "</div>" +
    "<div>"+ result['dispdlts_stcd'] + "</div>" +
    "</div>";
     return domstr;
}
function shipdlts_result_to_domstr(result) {
    var domstr = "<div class='shipdlts-search-result' data-shipdlts='" + JSON.stringify(result) + "'>"+
    "<div>"+ result['shipdlts_gstin'] + "</div>" +
    "<div>"+ result['shipdlts_lglnm'] + "</div>" +
    "<div>"+ result['shipdlts_trdnm'] + "</div>" +
    "<div>"+ result['shipdlts_address1'] + "</div>" +
    "<div>"+ result['shipdlts_address2'] + "</div>" +
    "<div>"+ result['shipdlts_loc'] + "</div>" +
    "<div>"+ result['shipdlts_pin'] + "</div>" +
    "<div>"+ result['shipdlts_stcd'] + "</div>" +

    "</div>";
     return domstr;
}


function shipdlts_result_click() {
    console.log("UPDATE THE FORM WITH SEARCH RESULT");
    shipdlts_data_json = JSON.parse($(this).attr('data-shipdlts'));
    $('#shipdlts-gstin-input').val(shipdlts_data_json['shipdlts_gstin']);
    $('#shipdlts-lglnm-input').val(shipdlts_data_json['shipdlts_lglnm']);
    $('#shipdlts-trdnm-input').val(shipdlts_data_json['shipdlts_trdnm']);
    $('#shipdlts-address1-input').val(shipdlts_data_json['shipdlts_address1']);
    $('#shipdlts-address2-input').val(shipdlts_data_json['shipdlts_address2']);
    $('#shipdlts-loc-input').val(shipdlts_data_json['shipdlts_loc']);
    $('#shipdlts-pin-input').val(shipdlts_data_json['shipdlts_pin']);
    $('#shipdlts-stcd-input').val(shipdlts_data_json['shipdlts_stcd']);
}

function dispdlts_result_click() {
    console.log("UPDATE THE FORM WITH SEARCH RESULT");
    dispdlts_data_json = JSON.parse($(this).attr('data-dispdlts'));
    $('#dispdlts-name-input').val(dispdlts_data_json['dispdlts_name']);
    $('#dispdlts-address1-input').val(dispdlts_data_json['dispdlts_address1']);
    $('#dispdlts-address2-input').val(dispdlts_data_json['dispdlts_address2']);
    $('#dispdlts-loc-input').val(dispdlts_data_json['dispdlts_loc']);
    $('#dispdlts-pin-input').val(dispdlts_data_json['dispdlts_pin']);
    $('#dispdlts-stcd-input').val(dispdlts_data_json['dispdlts_stcd']);
}


function initialize_fuse_dispdltss_search_bar() {
    console.log("INITIALIZING DISPDLTS SEARCH");

    $(".dispdlts_search_area").focusin(function() {
        $("#dispdlts_search_bar").show();
        var input = $('.dispdlts_search_input');
        var val = input.val();
        update_dispdlts_search_bar(val);
    });

    $(document).bind('focusin click',function(e) {
        if ($(e.target).closest('#dispdlts_search_bar, .dispdlts_search_area').length) return;
        $('#dispdlts_search_bar').hide();
    });

    $(".dispdlts_search_input").on("input", function(e) {
        $("#dispdlts_search_bar").show();
        var input = $(this);
        var val = input.val();
        update_dispdlts_search_bar(val);
    });
}

function initialize_fuse_shipdltss_search_bar() {
    console.log("INITIALIZING SHIPDLTS SEARCH");

    $(".shipdlts_search_area").focusin(function() {
        $("#shipdlts_search_bar").show();
        var input = $('.shipdlts_search_input');
        var val = input.val();
        update_shipdlts_search_bar(val);
    });

    $(document).bind('focusin click',function(e) {
        if ($(e.target).closest('#shipdlts_search_bar, .shipdlts_search_area').length) return;
        $('#shipdlts_search_bar').hide();
    });

    $(".shipdlts_search_input").on("input", function(e) {
        $("#shipdlts_search_bar").show();
        var input = $(this);
        var val = input.val();
        update_shipdlts_search_bar(val);
    });
}


function update_dispdlts_search_bar(search_string){
    console.log("Update dispdlts search bar with query: " + search_string);
    results = fuse_dispdltss.search(search_string);
    // console.log(results);
    $("#dispdlts_search_bar").empty();
    for (var i = 0; i < results.length; i++) {
        $("#dispdlts_search_bar").append(dispdlts_result_to_domstr(results[i]));
    }
    $('.dispdlts-search-result').click(dispdlts_result_click);
}
function update_shipdlts_search_bar(search_string){
    console.log("Update shipdlts search bar with query: " + search_string);
    results = fuse_shipdltss.search(search_string);
    // console.log(results);
    $("#shipdlts_search_bar").empty();
    for (var i = 0; i < results.length; i++) {
        $("#shipdlts_search_bar").append(shipdlts_result_to_domstr(results[i]));
    }
    $('.shipdlts-search-result').click(shipdlts_result_click);
}


function initialize_fuse_dispdltss () {
    // fetch dispdlts data
    $.getJSON( "/dispdltssjson", function( data ) {
        var fuse_dispdlts_options = {
            shouldSort: true,
            threshold: 0.6,
            location: 0,
            distance: 100,
            maxPatternLength: 32,
            minMatchCharLength: 1,
            keys: [
            "dispdlts_name",
            "dispdlts_address1",
            "dispdlts_address2",
            "dispdlts_loc",
            "dispdlts_pin",
            "dispdlts_stcd",
            ]
        };
        fuse_dispdltss = new Fuse(data, fuse_dispdlts_options);

        // initialize the search bar
        initialize_fuse_dispdltss_search_bar();
    });
}

function initialize_fuse_shipdltss () {
    // fetch shipdlts data
    $.getJSON( "/shipdltssjson", function( data ) {
        var fuse_shipdlts_options = {
            shouldSort: true,
            threshold: 0.6,
            location: 0,
            distance: 100,
            maxPatternLength: 32,
            minMatchCharLength: 1,
            keys: [
            "shipdlts_gstin",
            "shipdlts_lglnm",
            "shipdlts_trdnm",
            "shipdlts_address1",
            "shipdlts_address2",
            "shipdlts_loc",
            "shipdlts_pin",
            "shipdlts_stcd",
            ]
        };
        fuse_shipdltss = new Fuse(data, fuse_shipdlts_options);

        // initialize the search bar
        initialize_fuse_shipdltss_search_bar();
    });
}

// PRODUCT  AND ITEM SEARCH ========================================================

var selected_item_input;

function product_result_to_domstr(result) {
    var domstr = "<div class='product-search-result' data-product='" + JSON.stringify(result) + "'>"+
    "<div>"+ result['product_name'] + "</div>" +
    "<div>"+ result['product_hsn'] + " | " + result['product_unit'] + " | " + result['product_gst_percentage'] +
    "</div>";
     return domstr;
}

function item_result_to_domstr(result) {
    var domstr = "<div class='item-search-result' data-item='" + JSON.stringify(result) + "'>"+
    "<div>"+ result['item_slno'] + "</div>" +
    "<div>"+ result['item_prddesc'] + " | " + result['item_isservc'] +  " | " + result['item_hsncd'] +
    " | " + result['item_barcde'] +  " | " + result['item_qty'] +  " | " + result['item_freeqty'] +
    " | " + result['item_unit'] +  " | " + result['item_unitprice'] +  " | " + result['item_totamt'] +
    " | " + result['item_discount'] +  " | " + result['item_pretaxval'] +  " | " + result['item_assamt'] +
    " | " + result['item_gstrt'] +  " | " + result['item_igstamt'] +  " | " + result['item_cgstamt'] +
    " | " + result['item_sgstamt'] +  " | " + result['item_cesrt'] +  " | " + result['item_cesamt'] +
    " | " + result['item_cesnonadvlamt'] + " | " + result['item_statecesrt'] + " | " + result['item_statecesamt'] +
    " | " + result['item_statecesnonadvlamt'] + " | " + result['item_othchrg'] + " | " + result['item_totitemval'] +
    " | " + result['item_ordlineref'] + " | " + result['item_orgcntry'] + " | " + result['item_prdslno'] +
    "</div>";
     return domstr;
}

function initialize_fuse_product_search_bar() {
    console.log("INITIALIZING PRODUCT SEARCH");

    $(".product_search_area").focusin(function() {
        console.log("DISPLAY PRODUCT SEARCH");
        $("#product_search_bar").show();
        var input = $( this );
        selected_item_input = input;
        var val = input.val();
        update_product_search_bar(val);
    });

    $(document).bind('focusin click',function(e) {
        if ($(e.target).closest('#product_search_bar, .product_search_area').length) return;
        $('#product_search_bar').hide();
    });

    $(".product_search_input").on("input", function(e) {
        $("#product_search_bar").show();
        var input = $(this);
        var val = input.val();
        update_product_search_bar(val);
    });
}

function initialize_fuse_item_search_bar() {
    console.log("INITIALIZING Item SEARCH");

    $(".item_search_area").focusin(function() {
        console.log("DISPLAY ITEM SEARCH");
        $("#item_search_bar").show();
        var input = $( this );
        selected_item_input = input;
        var val = input.val();
        update_item_search_bar(val);
    });

    $(document).bind('focusin click',function(e) {
        if ($(e.target).closest('#item_search_bar, .item_search_area').length) return;
        $('#item_search_bar').hide();
    });

    $(".item_search_input").on("input", function(e) {
        $("#item_search_bar").show();
        var input = $(this);
        var val = input.val();
        update_item_search_bar(val);
    });
}

function update_product_search_bar(search_string){
    console.log("Update product search bar with query: " + search_string);
    results = fuse_products.search(search_string);
    console.log(results);
    $("#product_search_bar").empty();
    for (var i = 0; i < results.length; i++) {
        $("#product_search_bar").append(product_result_to_domstr(results[i]));
    }
    $('.product-search-result').click(product_result_click);
}

function update_item_search_bar(search_string){
    console.log("Update item search bar with query: " + search_string);
    results = fuse_items.search(search_string);
    console.log(results);
    $("#item_search_bar").empty();
    for (var i = 0; i < results.length; i++) {
        $("#item_search_bar").append(item_result_to_domstr(results[i]));
    }
    $('.item-search-result').click(item_result_click);
}

function initialize_fuse_products () {
    $.getJSON( "/productsjson", function( data ) {
        var fuse_product_options = {
            shouldSort: true,
            threshold: 0.6,
            location: 0,
            distance: 100,
            maxPatternLength: 32,
            minMatchCharLength: 1,
            keys: [
            "product_name",
            ]
        };
        fuse_products = new Fuse(data, fuse_product_options);
        // initialize the search bar
        initialize_fuse_product_search_bar();
    });
}


function initialize_fuse_items () {
    $.getJSON( "/itemsjson", function( data ) {
        var fuse_item_options = {
            shouldSort: true,
            threshold: 0.6,
            location: 0,
            distance: 100,
            maxPatternLength: 32,
            minMatchCharLength: 1,
            keys: [
            "item_slno",
            ]
        };
        fuse_items = new Fuse(data, fuse_item_options);
        // initialize the search bar
        initialize_fuse_item_search_bar();
    });
}


// START =============================================================

$(document).ready(function() {




    initialize_fuse_dispdltss();

    initialize_fuse_shipdltss();

    // Initialize product search
    initialize_fuse_products();

    initialize_fuse_items();

    // Initialize auto calculation of amounts
    initialize_auto_calculation();

});
