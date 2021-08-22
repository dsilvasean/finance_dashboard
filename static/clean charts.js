$(document).ready(function () {
    var table = $("#charts").DataTable({
        paging: false,
        // pageLength:100,
        responsive: true,
        scrollY:false,
        "initComplete":function(){
            $("#charts").show()
            $("#waitpage").hide()
            $("#charts_filter").hide()
            $("#searchbox").on("keyup search input paste cut", function() {
                table.search(this.value).draw();
             });   
            var tb_row = $('.tableRow')
            for (var i=0; i < tb_row.length; i++){
                if(tb_row[i].getAttribute('data-owned') == "True"){
               tb_row[i].style.fontWeight = "900";
            };
            };
            $("#colorCoding").change(function(){
              if (this.checked) {
                $(".tableRow td").removeClass("no_color_coding")
              }
              else{
                $(".tableRow td").addClass("no_color_coding")
              }
            });
        }
    })
    // add or remove from portfolio
    $("input#owned").change(function () {
        var this_row = this
        if (this.checked) {
            owned_modal = $("#owned_modal");
            owned_modal.modal('show');
            var buyPrice_modal = $('#buyPrice_modal')
            var ticker_modal = $('.ticker_modal')
            var form = $('#add_to_watchlist').attr('action', `addToIndex/${this_row.getAttribute('data-ticker')}/`)
            ticker_modal.attr('value', this.getAttribute('data-ticker'))
            buyPrice_modal.attr('value', this.getAttribute('data-current_price'))
            $('.closeModal').click(function () {
                this_row.checked = false;
            })

        }
        else {
            if (window.confirm(`Are you sure you want to remove ${this.getAttribute('data-ticker')} from your portfolio?`) == true) {
                // set csrf token
                $.ajaxSetup({
                    beforeSend: function (xhr, settings) {
                        function getCookie(name) {
                            var cookieValue = null;
                            if (document.cookie && document.cookie != '') {
                                var cookies = document.cookie.split(';');
                                for (var i = 0; i < cookies.length; i++) {
                                    var cookie = jQuery.trim(cookies[i]);
                                    // Does this cookie string begin with the name we want?
                                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                        break;
                                    }
                                }
                            }
                            return cookieValue;
                        }
                        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                            // Only send the token to relative URLs i.e. locally.
                            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                        }
                    }
                });
                $.ajax("./rmFromIndex",{
                    type:'POST',
                    data: { ticker: this.getAttribute('data-ticker')},
                    success:function(d){
                        window.location.href = d['url']
                    },
                    error:function(){
                        console.log('could not remove from portfolio...')
                    }
                });
                this_row.checked = false
            }
            else{
                this_row.checked = true
            }
        }
    });
    table_rows = $(".tableRow").click(function(evt){
        console.log(evt)
        if ( $(evt.target).is("input#owned") === false && $(evt.target).is("td.own_") === false ){
            console.log($(evt.target).is("input#owned"))
            var ticker = this.getAttribute('data-ticker');
            console.log(ticker)
            $('#imagemodal .modal-body img').attr('src', `${static}/charts/${ticker}.png`);
            $('#imagemodal .modal-header h3').html(ticker)
            $('#imagemodal').modal("show")
        }

    });
})