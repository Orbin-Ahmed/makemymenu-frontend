from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing),
    path('sign-in/', views.sign_in),  # sign-in
    path('sign-up/', views.sign_up),  # sign-Up
    path('verify/', views.verify),  # verify
    path('plans/', views.plans),  # select plans
    path('create-company/', views.create_company),  # create company
    path('create-branch/', views.create_branch),  # branch
    path('dashboard/', views.dashboard),  # Dashboard
    path('items/<item_id>/<bid>/', views.items),  # Item view
    path('combo-details/<combo_id>/<bid>/', views.combo_details),  # View item by id
    path('combo-details-update/<combo_id>/<bid>/', views.combo_details_update),  # View item by id
    path('combo-details-delete/<combo_id>/<bid>/', views.combo_details_delete),  # View item by id
    path('menu-details/<menu_id>/<bid>/', views.menu_details),  # view menu by menu id
    # path('primary-menu/<menu_branch_id>/', views.phone_view),  # the user view
    path('offer-menu/', views.offer_menu),
    path('reset-pass/<token>/', views.reset_password),
    path('reset-pass-email/', views.reset_email_verification),
    path('add-item/', views.add_item),
    path('contact-us/', views.contact_us),  # contact us without unauthorized
    path('user-update/<user_id>/', views.user_update),
    path('add-combo/', views.add_combo),  # create combo of multiple item
    path('company-update/<company_id>/', views.company_update),  # company info update
    path('add-branch/', views.add_branch),
    path('update-branch/', views.update_branch),  # add branch
    path('delete-branch/<bid>/', views.delete_branch),  # add branch
    path('delete-item/', views.delete_item),  # delete multiple item
    path('logout/', views.log_out, name='logout'),  # Logout
    path('change-package/', views.change_package),  # Change plans
    path('post-feedback/', views.post_feedback),  # post authorized feedback
    path('qr-create/', views.qr_create),  # menu qr create
    path('qr-wifi-create/', views.qr_wifi_create),  # Wi-Fi qr create
    path('create-menu/', views.create_menu),  # menu create
    path('user-sign-up/', views.user_sign_up),  # manager or owner new sign-up
    path('primary-menu/<bid>/<menu_id>/', views.set_primary_menu),  # primary menu set
    path('add-item-menu/<menu_id>/<bid>/', views.add_item_menu),  # add item to menu set
    path('delete-combo/', views.delete_combo),  # delete combo
    path('delete-menu-item/<menu_id>/<bid>/', views.delete_menu_item),  # delete menu item
    path('transfer-owner/<email_id>/', views.transfer_owner),
    path('service-terms/', views.conditions),
    path('get-stat-data/', views.get_stat),
    path('resend/', views.resend),
    path('image-to-excel/', views.image_to_excel),
    path('insert-items/', views.insert_items),
    path('update-multiple-item/', views.update_multiple_item),
    path('update-multiple-combo/', views.update_multiple_combo),
    path('primary-menu/<menu_branch_id>/', views.phone_menu),  # user menu view
    path('menu/item-details/<item_id>/<menu_id>/<menu_branch_id>/', views.phone_item_details),
    path('menu/combo-details/<group_id>/<menu_branch_id>/', views.phone_combo_details),
    path('add-promo/', views.add_promo),
    path('settings-system-update/', views.system_update),
    path('settings-change-log/', views.change_log),
    path('set-date-format/', views.set_date_format),
    path('update-localization/', views.update_localization),
    path('item-image-remove/<item_id>/<bid>/', views.item_image_remove),
    path('combo-image-remove/<combo_id>/<bid>/', views.combo_image_remove),
    path('remove-promo/<bid>/', views.remove_promo),
    path('privacy-policies/', views.privacy),
]
