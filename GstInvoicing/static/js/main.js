var invoice_item_row_counter = 1
var fuse_dispdlts;
var fuse_shipdlts;

// ADDING INVOICE ROWS ===================================================
function add_invoice_item_row() {
    old_item_row_count = invoice_item_row_counter
    invoice_item_row_counter++;

    $('#invoice-form-items-table-body >tr:last').clone(true).insertAfter('#invoice-form-items-table-body >tr:last');
    $('#invoice-form-items-table-body >tr:last input').val('');

    $('#invoice-form-items-table-body >tr:last td')[0].innerHTML = invoice_item_row_counter
    update_amounts($('#invoice-form-items-table-body input[name=invoice-qty]:last'));
}

function setup_invoice_rows() {
    $("#invoice-form-addrow").click(function(event) {
       event.preventDefault();
       add_invoice_item_row();
    });

    for (var i = 0; i <= 4; i++) {
        add_invoice_item_row();
    }
}

// UPDATING INVOICE TOTALS ================================================

function update_invoice_totals() {

    // amount without gst
    sum_amt_without_gst = 0
    $('input[name=invoice-amt-without-gst]').each(function(){
        sum_amt_without_gst += parseFloat($(this).val());
    });
    $('input[name=invoice-total-amt-without-gst]').val(sum_amt_without_gst.toFixed(2));

    // amount sgst
    sum_amt_sgst = 0
    $('input[name=invoice-amt-sgst]').each(function(){
        sum_amt_sgst += parseFloat($(this).val());
    });
    $('input[name=invoice-total-amt-sgst]').val(sum_amt_sgst.toFixed(2));

    // amount cgst
    sum_amt_cgst = 0
    $('input[name=invoice-amt-cgst]').each(function(){
        sum_amt_cgst += parseFloat($(this).val());
    });
    $('input[name=invoice-total-amt-cgst]').val(sum_amt_cgst.toFixed(2));

    // amount igst
    sum_amt_igst = 0
    $('input[name=invoice-amt-igst]').each(function(){
        sum_amt_igst += parseFloat($(this).val());
    });
    $('input[name=invoice-total-amt-igst]').val(sum_amt_igst.toFixed(2));

    sum_amt_with_gst = 0
    $('input[name=invoice-amt-with-gst]').each(function(){
        sum_amt_with_gst += parseFloat($(this).val());
    });
    $('input[name=invoice-total-amt-with-gst]').val(sum_amt_with_gst.toFixed(2));

}


// AUTO CALCULATE ITEM AMOUNTS =============================================

function initialize_auto_calculation(){
    update_amounts($('#invoice-form-items-table-body input[name=invoice-qty]:first'));
    $('input[name=invoice-qty], input[name=invoice-gst-percentage], input[name=invoice-rate-with-gst]').change(function (){
        update_amounts($(this));
    });
}

function update_amounts(element){
    var product = element.parent().parent().find('input[name=invoice-product]').val();
    var qty = parseInt(element.parent().parent().find('input[name=invoice-qty]').val());
    var rate_with_gst = parseFloat(element.parent().parent().find('input[name=invoice-rate-with-gst]').val());
    var gst_percentage = parseFloat(element.parent().parent().find('input[name=invoice-gst-percentage]').val());

    var rate_without_gst = (rate_with_gst * 100.0) / (100.0 + gst_percentage);
    var amt_without_gst = rate_without_gst * qty;

    var sgst;
    var cgst;
    var igst;
    if(product == ""){
        sgst = 0;
        cgst = 0;
        igst = 0;
        amt_without_gst = 0;
    }
    else {
        if($('input[name=igstcheck]').is(':checked')){
            sgst = 0;
            cgst = 0;
            igst = amt_without_gst * gst_percentage / 100;
        }
        else {
            sgst = amt_without_gst * gst_percentage / 200;
            cgst = amt_without_gst * gst_percentage / 200;
            igst = 0;

        }
    }
    var amt_with_gst = amt_without_gst + cgst + sgst + igst;

    element.parent().parent().find('input[name=invoice-rate-without-gst]').val(rate_without_gst.toFixed(2));
    element.parent().parent().find('input[name=invoice-amt-without-gst]').val(amt_without_gst.toFixed(2));
    element.parent().parent().find('input[name=invoice-amt-sgst]').val(sgst.toFixed(2));
    element.parent().parent().find('input[name=invoice-amt-cgst]').val(cgst.toFixed(2));
    element.parent().parent().find('input[name=invoice-amt-igst]').val(igst.toFixed(2));
    element.parent().parent().find('input[name=invoice-amt-with-gst]').val(amt_with_gst.toFixed(2));

    update_invoice_totals();

}




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
function product_result_click() {
    console.log("UPDATE THE FORM WITH SEARCH RESULT");
    product_data_json = JSON.parse($(this).attr('data-product'));
    selected_item_input.val(product_data_json['product_name']);
    selected_item_input.parent().parent().find('input[name=invoice-hsn]').val(product_data_json['product_hsn']);    
    selected_item_input.parent().parent().find('input[name=invoice-unit]').val(product_data_json['product_unit']);    
    selected_item_input.parent().parent().find('input[name=invoice-rate-with-gst]').val(product_data_json['product_rate_with_gst']);    
    selected_item_input.parent().parent().find('input[name=invoice-gst-percentage]').val(product_data_json['product_gst_percentage']);    

}

function item_result_click() {
    console.log("UPDATE THE FORM WITH SEARCH RESULT");
    item_data_json = JSON.parse($(this).attr('data-item'));
    selected_item_input.val(item_data_json['item_slno']);
    selected_item_input.parent().parent().find('input[name=invoice-prddesc]').val(item_data_json['item_prddesc']);    
    selected_item_input.parent().parent().find('input[name=invoice-isservc]').val(item_data_json['item_isservc']);    
    selected_item_input.parent().parent().find('input[name=invoice-hsncd]').val(item_data_json['item_hsncd']);    
    selected_item_input.parent().parent().find('input[name=invoice-barcde]').val(item_data_json['item_barcde']);    
    selected_item_input.parent().parent().find('input[name=invoice-qty]').val(item_data_json['item_freeqty']);    
    selected_item_input.parent().parent().find('input[name=invoice-unit]').val(item_data_json['item_unit']);    
    selected_item_input.parent().parent().find('input[name=invoice-unitprice]').val(item_data_json['item_unitprice']);    
    selected_item_input.parent().parent().find('input[name=invoice-totamt]').val(item_data_json['item_totamt']);    
    selected_item_input.parent().parent().find('input[name=invoice-discount]').val(item_data_json['item_discount']);    
    selected_item_input.parent().parent().find('input[name=invoice-pretaxval]').val(item_data_json['item_pretaxval']);    
    selected_item_input.parent().parent().find('input[name=invoice-assamt]').val(item_data_json['item_assamt']);    
    selected_item_input.parent().parent().find('input[name=invoice-gstrt]').val(item_data_json['item_gstrt']);    
    selected_item_input.parent().parent().find('input[name=invoice-cgstamt]').val(item_data_json['item_cgstamt']);    
    selected_item_input.parent().parent().find('input[name=invoice-sgstamt]').val(item_data_json['item_sgstamt']);    
    selected_item_input.parent().parent().find('input[name=invoice-icesrt]').val(item_data_json['item_cesrt']);    
    selected_item_input.parent().parent().find('input[name=invoice-cesamt]').val(item_data_json['item_cesamt']);    
    selected_item_input.parent().parent().find('input[name=invoice-cesnonadvlamt]').val(item_data_json['item_cesnonadvlamt']);    
    selected_item_input.parent().parent().find('input[name=invoice-statecesrt]').val(item_data_json['item_statecesrt']);    
    selected_item_input.parent().parent().find('input[name=invoice-statecesamt]').val(item_data_json['item_statecesamt']);    
    selected_item_input.parent().parent().find('input[name=invoice-statecesnonadvlamt]').val(item_data_json['item_statecesnonadvlamt']);    
    selected_item_input.parent().parent().find('input[name=invoice-othchrg]').val(item_data_json['item_othchrg']);    
    selected_item_input.parent().parent().find('input[name=invoice-totitemval]').val(item_data_json['item_totitemval']);    
    selected_item_input.parent().parent().find('input[name=invoice-ordlineref]').val(item_data_json['item_ordlineref']); 
    selected_item_input.parent().parent().find('input[name=invoice-orgcntry]').val(item_data_json['item_orgcntry']);   
    selected_item_input.parent().parent().find('input[name=invoice-prdslno]').val(item_data_json['item_PrdSlNo']);    

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
    // fetch customer data
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
    // fetch customer data
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

    // Initialize invoice row addition
    setup_invoice_rows();

    // Initialize customer search

    initialize_fuse_dispdltss();

    initialize_fuse_shipdltss();

    // Initialize product search
    initialize_fuse_products();

    initialize_fuse_items();

    // Initialize auto calculation of amounts
    initialize_auto_calculation();

    // Initialize igst toggle
    $("input[name=igstcheck]").change(function() {
            $('input[name=invoice-qty]').each(function(){
                update_amounts($( this ));
            });
    });

    // Show the invoice form
    $("#invoice-form")[0].hidden = false;

});
