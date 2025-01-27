<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    {% include 'admin/layouts/meta.html' %}
    {% include 'admin/layouts/styles.html' %}
    <link rel="icon" href="{{ asset(\App\ImageManager::resize($sitelogo->orderedItems[0]->image, {'width': 124, 'height': 124})) }}" type="image/x-icon">
    {% block meta %}{% endblock %}
    {% block styles %}{% endblock %}
    <style>
    .content-col.col-lg-11 {
    width: 91.66666667% !important;
}
        .spinner {
            margin: 300px auto;
            width: 40px;
            height: 40px;
            position: relative;
            text-align: center;
            top: 50%;
            -webkit-animation: sk-rotate 2.0s infinite linear;
            animation: sk-rotate 2.0s infinite linear;
        }

        .dot1, .dot2 {
            width: 60%;
            height: 60%;
            display: inline-block;
            position: absolute;
            top: 0;
            background-color: #333;
            border-radius: 100%;

            -webkit-animation: sk-bounce 2.0s infinite ease-in-out;
            animation: sk-bounce 2.0s infinite ease-in-out;
        }

        .dot2 {
            top: auto;
            bottom: 0;
            -webkit-animation-delay: -1.0s;
            animation-delay: -1.0s;
        }

        @-webkit-keyframes sk-rotate { 100% { -webkit-transform: rotate(360deg) }}
        @keyframes sk-rotate { 100% { transform: rotate(360deg); -webkit-transform: rotate(360deg) }}

        @-webkit-keyframes sk-bounce {
            0%, 100% { -webkit-transform: scale(0.0) }
            50% { -webkit-transform: scale(1.0) }
        }

        @keyframes sk-bounce {
            0%, 100% {
                transform: scale(0.0);
                -webkit-transform: scale(0.0);
            } 50% {
                  transform: scale(1.0);
                  -webkit-transform: scale(1.0);
              }
        }
        .modal-static {
            position: fixed;
            overflow: visible !important;
        }
        .modal-static,
        .modal-static .modal-dialog,
        .modal-static .modal-content {
            width: 100%;
        }
        .modal-static .modal-dialog,
        .modal-static .modal-content {
            padding: 0 !important;
            margin: 0 !important;
        }
    </style>
</head>
<body class="hold-transition skin-purple-light sidebar-mini">
<div class="modal modal-static fade" id="processing-modal" role="dialog" aria-hidden="true" data-keyboard="false" data-backdrop="static">
<div class="modal modal-static fade" id="processing-modal" role="dialog" aria-hidden="true" data-keyboard="false" data-backdrop="static">
    <div class="modal-dialog">
        <div class="spinner">
            <div class="dot1"></div>
            <div class="dot2"></div>
        </div>
    </div>
</div>
<div class="wrapper">

    {% include 'admin/layouts/header.html' %}
    <!-- Left side column. contains the logo and sidebar -->


  <div class="container-fluid main-container">
      <div class="row">
            <div class="col-lg-2 col-md-4 col-xs-12 p-0 side-col">
                {% include 'admin/layouts/sidebar.html' %}
            </div>
          <div class="col-lg-10 col-md-8 col-xs-12 content-col pl-0">
                  <!-- Content Wrapper. Contains page content -->
    <div class="content-wrapper">
        <!-- Content Header (Page header) -->
        {{-- <section class="content-header">
           <h1>
                {{ $site_settings['title'] }}
                <small>پنل مدیریت</small>
            </h1>
            <ol class="breadcrumb">--}}
                {{--<li><a href="#"><i class="fa fa-dashboard"></i> پنل مدیریت</a></li>--}}
                {{--<li><a href="#">بخش واسطه</a></li>--}}
                {{--<li class="active">بخش جاری</li>--}}
            {{--</ol>
        </section>
--}}

                    {% include 'admin/layouts/partials/callout.html' %}
                    {% include 'admin/layouts/partials/input-errors.html' %}


        <!-- Main content -->
        <section class="content">
                        {% block content %}{% endblock %}

        </section>
        <!-- /.content -->
    </div>
    <!-- /.content-wrapper 
    <footer class="main-footer">
        <div class="pull-right hidden-xs">
            <span>{{ $site_settings['copyright'] }} </span>
        </div>
     
    </footer>-->
          </div>
      </div>
  </div>
</div>
<!-- ./wrapper -->
    {% include 'admin/layouts/scripts.html' %}
    {% include 'admin/layouts/partials/message.html' %}
    {% block scripts %}{% endblock %}

<script>
     $('.sidebar-toggle').click( function () {
       $('.side-col').toggleClass('col-lg-1 col-md-2');	
        $('.content-col').toggleClass('col-lg-11 col-md-10');	
	});
</script>
</body>
</html>
