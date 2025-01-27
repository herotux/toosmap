<header class="main-header"><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <!-- Logo -->
    <a href="{{ route('home') }}" class="logo">
        <!-- mini logo for sidebar mini 50x50 pixels -->
        <span class="logo-mini"><b>G</b>D</span>
        <!-- logo for regular state and mobile devices -->
        <span class="logo-lg"><b>{{ $site_settings['title'] }}</b></span>
    </a>
    <!-- Header Navbar: style can be found in header.less -->
    <nav class="navbar navbar-static-top">
        <!-- Sidebar toggle button-->
        <a href="#" class="sidebar-toggle" data-toggle="offcanvas" role="button">
            <span class="sr-only">Toggle navigation</span>
        </a>

        <div class="navbar-custom-menu">
            <ul class="nav navbar-nav">
                @if($loggedin_user->hasRole('admin'))
                <li class="dropdown notifications-menu">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                      <i class="fa fa-eye"></i>
                      <span class="label label-warning">{{ $site_settings['site_views'] }}</span>
                    </a>
                </li>
                @endif
                @if($loggedin_user->can('orders-manage'))
                <li class="notifications-menu">
                    <a href="{{ route('admin.orders.index') }}">
                        <i class="fa fa-shopping-basket"></i>
                        <span class="label label-warning">{{ $waitingOrders }}</span>
                    </a>
                </li>
                @endif
                <!-- User Account: style can be found in dropdown.less -->
                <li class="dropdown user user-menu">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                        <img src="{{ $loggedin_user->avatar }}" class="user-image" alt="User Image">
                        <span class="hidden-xs">{{ $loggedin_user->name }}</span>
                    </a>
                    <ul class="dropdown-menu">
                        <!-- User image -->
                        <li class="user-header">
                            <img src="{{ $loggedin_user->avatar }}" class="img-circle" alt="User Image">

                            <p>
                                {{ $loggedin_user->roles()->first()->display_name }}
                                <small>عضویت در {{ jdate($loggedin_user->created_at)->format('d F Y ساعت H:i') }}</small>
                            </p>
                        </li>
                        <!-- Menu Body -->
                        <li class="user-body">
                            <div class="row">
                                @if($loggedin_user->can('manage-store'))
                                <div class="col-xs-4 text-center">
                                    <a href="{{ route('admin.categories.index') }}">دسته‌بندی‌ها</a>
                                </div>
                                @endif
                                @if($loggedin_user->can('products-manage'))
                                <div class="col-xs-4 text-center">
                                    <a href="{{ route('admin.products.index') }}">محصولات</a>
                                </div>
                                @endif
                                @if($loggedin_user->can('orders-manage'))
                                <div class="col-xs-4 text-center">
                                    <a href="{{ route('admin.orders.index') }}">سفارش‌ها</a>
                                </div>
                                @endif
                            </div>
                            <!-- /.row -->
                        </li>
                        <!-- Menu Footer-->
                        <li class="user-footer">
                            <div class="pull-left">
                                <a href="{{ route('accounts.dashboard') }}" class="btn btn-default btn-flat">پنل کاربری</a>
                            </div>
                            <div class="pull-right">
                                <a href="{{ route('logout') }}" onclick="event.preventDefault();
                                                     document.getElementById('logout-form').submit();"
                                   class="btn btn-default btn-flat"><span>خروج</span>
                                </a>
                                <form id="logout-form" action="{{ route('logout') }}" method="POST" style="display: none;">
                                    @csrf
                                </form>
                            </div>
                        </li>
                    </ul>
                </li>
            </ul>
        </div>
    </nav>
</header>
