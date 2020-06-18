from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode
from mqbproductivity.models import TasksTracking, Daily, Effort, BlockData, TaskCategory
from management.models import Holiday, MonthlyProductivity
import datetime
from datetime import datetime as datet
from django.contrib.auth.models import Group, User
# Create your views here.


def homepage(request):
    if request.method == 'POST':
        if 'queryMonth' in request.POST:
            selecteddate = request.POST['startDate'].replace(' ', '_')
            date_contain = {
                'month': selecteddate,
            }
            base_url = reverse('home')
            query_string = urlencode(date_contain)
            url = '{}?{}'.format(base_url, query_string)
            return HttpResponseRedirect(url)

    if request.user.is_superuser:  # Check superuser can access to all groups
        groups = Group.objects.all()
    else:
        groups = request.user.groups.all()

    if 'month' in request.GET:
        selectdate = datet.strptime(request.GET.get('month'), '%B_%Y').date()
    else:
        selectdate = datetime.date.today()

    startdateOfmonth = (selectdate.replace(day=1))  # get start date of month
    enddateOfmonth = datetime.date(selectdate.year + selectdate.month // 12,
                                   selectdate.month % 12 + 1, 1) - datetime.timedelta(1)  # get end date of month

    # get working date in month base on Holiday list.
    # Saturday and Sunday are not working date
    num_date_working = 0
    holidays = Holiday.objects.all()
    holidays_list = list()
    for h in holidays:
        holidays_list.append(h.date)

    date_in_month = startdateOfmonth
    while date_in_month <= enddateOfmonth:
        if date_in_month not in holidays_list and date_in_month.strftime("%A") not in ['Sunday', 'Saturday']:
            num_date_working += 1
        date_in_month += datetime.timedelta(1)

    num_hour_working = num_date_working*8
    # print('num_date_working: ', num_date_working)
    # print('num_hour_working: ', num_hour_working)
    # -----------end------------

    dates = Daily.objects.filter(date__range=[startdateOfmonth, enddateOfmonth])
    data_product = dict()
    pie_chart_effort = dict()
    pie_chart_PyS = dict()
    if groups:
        for group in groups:
            users = User.objects.filter(groups__name=group)
            tasks = list()
            for d in dates:
                tasks.append(Effort.objects.filter(dateCreateTask=d).filter(member__in=users))
            # efforts = list()
            # for ts in tasks:
            #     temp = list()
            #     for t in ts:
            #         temp.append(Effort.objects.get(task=t))
            #     efforts.append(temp)
            #     del temp

            task_list = list(TaskCategory.objects.all())
            sumeffort = {}
            sumlist = [['Category', 'Total_TC(TC)', 'Total_Eff(h)']]
            sum_tc = 0
            sum_eff = 0
            efforts_per_month = [['Categories', 'Effort']]
            Pys_per_month = [['Categories', 'TC']]
            sum_eff_per_month = 0
            for t in task_list:
                totaltc = 0
                totale = 0
                for eff in tasks:
                    for e in eff:
                        if e.tasktracking.categories.name == t.name:
                            totaltc += e.quantity
                            totale += e.effort
                            sum_tc += e.quantity
                            sum_eff += e.effort
                sumeffort[t.name] = [totaltc, totale]
                sumlist.append([t.name, totaltc, totale])
                
                efforts_per_month.append([t.name, (totale/num_hour_working)])
                sum_eff_per_month += totale/num_hour_working

                # update info for PyS chart
                if totale/num_hour_working != 0:
                    pys = totaltc/(totale/num_hour_working)/num_date_working
                else:
                    pys = 0
                Pys_per_month.append([t.name, pys])

            # update info for task non-project
            # if sum_eff_per_month != 0:
            #     efforts_per_month.append(["Non-Project", (len(users)-sum_eff_per_month)])

            data_product[group.name] = sumlist
            pie_chart_effort[group.name] = efforts_per_month
            pie_chart_PyS[group.name] = Pys_per_month

        contain = {
            'sumeffort': sumeffort,
            'sum_tc': sum_tc,
            'sum_eff': sum_eff,
            'selectDate': startdateOfmonth,
            'sumlist': sumlist,
            'data_product': data_product,
            'num_hour_working': num_hour_working,
            'num_date_working': num_date_working,
            'pie_chart_effort': pie_chart_effort,
            'pie_chart_PyS': pie_chart_PyS,
        }
    else:
        # if user doesn't belong to any group
        contain = {
            'notification': 'You are not in any group. Please contact Administrator!!!'
        }
    return render(request, "home.html", contain)
