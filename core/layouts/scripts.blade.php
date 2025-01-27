<!-- jQuery 2.2.3 -->
<script src="{{ asset('dashboard/plugins/jQuery/jquery-2.2.3.min.js') }}"></script>
<!-- Bootstrap 3.3.6 -->
<script src="{{ asset('dashboard/bootstrap/js/bootstrap.min.js') }}"></script>
<!-- FastClick -->
<script src="{{ asset('dashboard/plugins/fastclick/fastclick.js') }}"></script>
<!-- AdminLTE App -->
<script src="{{ asset('dashboard/dist/js/app.min.js') }}"></script>
<!-- AdminLTE for demo purposes -->
{{--<script src="/dashboard/dist/js/demo.js"></script>--}}
{{--<script src="/dashboard/dist/js/dashboard.js"></script>--}}
<script src="{{ asset('dashboard/plugins/izitoast/js/iziToast.min.js') }}" type="text/javascript"></script>
<!--<script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>-->
<!--<script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>-->
<script src="{{ asset('vendor/tinymce/js/tinymce/tinymce.min.js') }}"></script>
<script>
    var editor_config = {
        path_absolute : "/",
        selector: "textarea.tinymce",
        plugins: [
            "advlist autolink lists link image charmap print preview hr anchor pagebreak",
            "searchreplace wordcount visualblocks visualchars code fullscreen",
            "insertdatetime media nonbreaking save table contextmenu directionality",
            "emoticons template paste textcolor colorpicker textpattern"
        ],
        directionality: 'rtl',
        toolbar: "insertfile undo redo | rtl ltr | styleselect | fontsizeselect | forecolor backcolor | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image media",
        fontsize_formats: '11px 12px 14px 16px 18px 24px 36px 48px',
        relative_urls: false,
        file_browser_callback : function(field_name, url, type, win) {
            var x = window.innerWidth || document.documentElement.clientWidth || document.getElementsByTagName('body')[0].clientWidth;
            var y = window.innerHeight|| document.documentElement.clientHeight|| document.getElementsByTagName('body')[0].clientHeight;

            var cmsURL = editor_config.path_absolute + 'laravel-filemanager?field_name=' + field_name;
            if (type == 'image') {
                cmsURL = cmsURL + "&type=Images";
            } else {
                cmsURL = cmsURL + "&type=Files";
            }

            tinyMCE.activeEditor.windowManager.open({
                file : cmsURL,
                title : 'Filemanager',
                width : x * 0.8,
                height : y * 0.8,
                resizable : "yes",
                close_previous : "no"
            });
        },
        language : 'fa_IR',
    };

    tinymce.init(editor_config);
</script>
<script>
    $(document).ready(function(){
        $('.pagination').addClass("pagination-sm no-margin pull-right");
        $('.close-callout').click(function () {
            $(this).parentsUntil('.pad').remove();
        });
    });
</script>
<script>
    $(document).ready(function () {
        $('.close-callout').click(function () {
            $(this).parentsUntil('.pad').remove();
        });
    });
</script>
