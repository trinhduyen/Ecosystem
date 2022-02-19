from tempfile import template
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from .models import Sale
from sales.forms import SalesSearchForm
from reports.forms import ReportForm
import pandas as pd
from sales.utils import get_customer_from_id, get_saleman_from_id, get_chart
# Create your views here.

# start part 19


def home_view(request):
    sale_df = None
    positions_df = None
    merged_df = None
    df = None
    chart = None
    no_data=None
    
    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()
    
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')
        #print(date_from, date_to, chart_type)
        '''
        $lt  giá trị phải nhỏ hơn điều kiện
        $gt  giá trị phải lớn hơn điều kiện
        $lte  giá trị phải nhỏ hơn hoặc bằng điều kiện
        $gte  giá trị phải lớn hơn hoặc bằng điều kiện
        $in  giá trị phải nằm trong tập điều kiện
        $nin  giá trị phải không nằm trong tập điều kiện
        $not  giá trị không nắm trong điều kiện
        '''
        sales_qs = Sale.objects.filter(created__date__lte=date_to,
                                       created__date__gte=date_from)
        #obj = Sale.objects.get(id=1)
        if len(sales_qs) > 0:
            sale_df = pd.DataFrame(sales_qs.values())
            sale_df['customer_id'] = sale_df['customer_id'].apply(
                get_customer_from_id)
            sale_df['salesman_id'] = sale_df['salesman_id'].apply(
                get_saleman_from_id)
            sale_df['created'] = sale_df['created'].apply(
                lambda x: x.strftime('%d/%m/%Y'))
            # rename
            #sale_df = sale_df.rename({'customer_id': 'customer','salesman_id': 'salesman'}, axis=1)
            sale_df.rename({'customer_id': 'customer',
                            'salesman_id': 'salesman', 'id': 'sales_id'}, axis=1, inplace=True)
            position_data = []
            for sale in sales_qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sales_id': pos.get_sales_id(),
                    }
                    position_data.append(obj)
            positions_df = pd.DataFrame(position_data)
            merged_df = pd.merge(sale_df, positions_df, on='sales_id')
            df = merged_df.groupby('transaction_id', as_index=False)[
                'price'].agg('sum')

            chart = get_chart(chart_type, sale_df, results_by)
            #print('Position df')
            # print(positions_df)

            sale_df = sale_df.to_html()
            positions_df = positions_df.to_html()
            merged_df = merged_df.to_html()
            df = df.to_html()

        else:
            no_data='No date is available in this range'

    context = {
        'search_form': search_form,
        'report_form': report_form,
        'sale_df': sale_df,
        'positions_df': positions_df,
        'merged_df': merged_df,
        'df': df,
        'chart': chart,
        'no_data':no_data,
    }
    return render(request, 'sales/home.html', context)


class SaleListView(ListView):
    model = Sale
    template_name = 'sales/main.html'

# Hoặc có thể viết theo dạng Function


def sale_list_view(request):
    qs = Sale.objects.all()
    return render(request, 'sales/main.html', {'object_list': qs})


class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'
# hoặc có thể viết như sau


def sale_detail_view(request, **kwargs):
    pk = kwargs.get['pk']
    obj = Sale.objects.get(pk=pk)
    # or
    #obj = get_object_or_404(pk=pk)
    return render(request, 'sales/detail.html', {'object': obj})


'''
    khi đó trong file urls

    path('sales/', sale_list_view, name='list'),
    path('sales/<pk>/', sale_detail_view, name='detail'),
'''
