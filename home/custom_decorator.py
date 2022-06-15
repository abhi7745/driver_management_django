from django.shortcuts import redirect




# main user role manager function for [admin, driver ]
def role_required_decorator(allowed_roles=[]):
    def decorator(view_fun):
        def wrap(request,*args, **kwargs):

            if request.user.role:
                # main check case
                if request.user.role in allowed_roles:
                    print(request.user.role,'==', allowed_roles)
                    print('from role_required_decorator')
                    return view_fun(request, *args, **kwargs)

                else:
                    print('not ok - from role_required_decorator')
                    print(request.user.role,'role')
                    return redirect('/')
            else:
                print('query not exist - from role_required_decorator')
                print(request.user.role)
                return redirect('/')

                

        return wrap

    return decorator