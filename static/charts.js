$(document).ready(function (){
    var count = 0;
    var table = $('#charts').DataTable({
        // paging: false,
        responsive:true,
      });
    // window.alert("hello")
    var owned_check = []
    data_ = document.querySelectorAll('input#owned')
    console.log(data_[0])
    $('input#owned').change(function (){
        var this_row = this
        if (this_row.checked){
            $('#owned_modal').modal('show')
            var input_to_highlight = $('.highlight')
            var buyPrice_modal = $('#buyPrice_modal')
            var ticker_modal = $('.ticker_modal')
            var form = $('#add_to_watchlist').attr('action', `addToIndex/${this_row.getAttribute('data-ticker')}/`)
            ticker_modal.attr('value', this.getAttribute('data-ticker'))
            buyPrice_modal.attr('value', this.getAttribute('data-current_price'))
            window.setTimeout(function(){
                // input_to_highlight.focus()
                // input_to_highlight.select()
            },1000)
            // console.log(`${y}-${m}-${d}, ${typeof(m)}`)
            $('.closeModal').click(
                function(){
                    console.log(this_row)
                    this_row.checked = false;
                    console.log(this_row.checked)
                }
            )
        }
       else {
           
        if (window.confirm(`Are you sure you want to remove ${this.getAttribute('data-ticker')} from your portfolio?`)== true){
            $.ajaxSetup({ 
                beforeSend: function(xhr, settings) {
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
            $.ajax('./rmFromIndex', {
                type: 'POST',
                data: { ticker: this.getAttribute('data-ticker')},
                success: function(d){
                    console.log(d)
                    window.location.href = d['url']
                },
                error: function(){
                    console.log('error')
                }
            });
            this_row.checked = false
        }
        else {
            this.checked = true
        }
       }
    })
    // console.log(_data_)
    var table_row  = $('.tableRow')
    $(".tableRow").click(function(){
        var ticker = this.getAttribute('data-ticker')
        $("#chart_modal").modal("show")
        var load = "{% load static %}"
        $("#chart_modal div.modal-body img").attr("src", `${static}/charts/${ticker}.png`)
    })
    for (var i =0; i < table_row.length; i++){
        if (table_row[i].getAttribute('data-owned') =='True'){
            table_row[i].style.fontWeight = "bold"
        }
        else{
            count++;
            console.log(count)
        }
    }
   
})

