from django.shortcuts import render
from django.contrib.auth.models import User
from . import models
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from urllib.parse import urlencode
import datetime
from datetime import datetime as datet
import re
# Create your views here.


def add_effort(user_id, date_create_task, task_obj, quantity, effort, comment):
    update_effort = models.Effort(
            member=user_id,
            dateCreateTask=date_create_task,
            tasktracking=task_obj,
            quantity=quantity,
            effort=effort,
            comment=comment
    )
    update_effort.save()
    return update_effort


def productivity_index(request):
    #user_id = User.objects.get(pk=pk)

    user_id = User.objects.get(username=request.user)
    print("user request")
    print(user_id)
    if request.method == 'POST':
        
        if request.is_ajax():
            print(request.POST)
            if 'delete_task' in request.POST:
                models.Effort.objects.filter(id=request.POST.get('delete_task')).delete()
                contain = {
                    'success': True,
                }
                return JsonResponse(contain)

            elif 'add_task' in request.POST:
                data = dict(request.POST)
                try:
                    update_date = models.Daily(
                        date=request.POST['date'],
                    )
                    update_date.save()
                except Exception as e:
                    print(e)
                    print("date is already existed")
                print(data)
                for i, task in enumerate(data['task']):
                    tasktracking = models.TasksTracking.objects.get(id=int(task))
                    add_effort(user_id, update_date, tasktracking, data['quantity'][i], data['effort'][i], data['comment'][i])
                contain = {
                    'success': True,
                }
                return JsonResponse(contain)
            
            elif 'edit_task' in request.POST:
                data = dict(request.POST)
                for i, effortID in enumerate(data['effortID']):

                    task_list_id = int(data['task_list'][i])
                    task_l = models.TasksTracking.objects.get(id=task_list_id)
                    models.Effort.objects.filter(pk=int(effortID)).update(
                        tasktracking=task_l,
                        quantity=data['quantity'][i],
                        effort=data['effort'][i],
                        comment=data['comment'][i],
                    )

                contain = {
                    'success': True,
                }
                return JsonResponse(contain)

        elif 'querydate' in request.POST:
            date_contain = {
                'startdate': request.POST['start_date'],
                'enddate': request.POST['end_date']
            }
            base_url = reverse('productivity_index')
            query_string = urlencode(date_contain)
            url = '{}?{}'.format(base_url, query_string)
            return HttpResponseRedirect(url)

    # get days in current week
    date = datetime.date.today()
    if 'startdate' in request.GET and 'enddate' in request.GET:
        start_week = datet.strptime(request.GET.get('startdate'), '%Y-%m-%d')
        end_week = datet.strptime(request.GET.get('enddate'), '%Y-%m-%d')
    else:
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(6)
    ######################
    # print(start_week)
    # print(end_week)
    add_date = models.Daily()
    dt = start_week
    while dt <= end_week:
        try:
            add_date.date = dt
            add_date.save()
            dt += datetime.timedelta(1)
        except Exception as e:
            print('add date!!!!!!!!!!!!!!!!!!!!!!!')
            print(e)

    dates = models.Daily.objects.filter(date__range=[start_week, end_week])
    tasks = list()
    #tasks_test = list()
    dates.reverse()
    for d in dates:
        temp = models.Effort.objects.filter(dateCreateTask=d).filter(member=user_id)
        tasks.append(temp)
        # if len(temp):
        #     for t in temp:
        #         tasks_test.append([
        #             t.id,
        #             datet.strftime(d.date, '%A_%d_%b_%Y'), 
        #             t.tasktracking.categories.name,
        #             t.tasktracking.taskName,
        #             t.quantity,
        #             t.effort,
        #             t.comment
        #         ])
        # else:
        #     tasks_test.append([
        #         'new',
        #         datet.strftime(d.date, '%A_%d_%b_%Y'),'','','','','',
        #     ])

    # efforts = list()
    # for ts in tasks:
    #     temp = list()
    #     for t in ts:
    #         temp.append(t)
    #     efforts.append(temp)
    #     del temp

    efforts_dict = dict(zip(dates, tasks))

    task_list = list(models.TaskCategory.objects.all())
    sumeffort = {}
    pys = []
    sum_tc = 0
    sum_eff = 0
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
        if totale == 0:
            pys.append(0)
        else:
            pys.append(round(totaltc/(totale/8),2)) # 8 hour working/day

    # get start day and end date of month
    startdateOfmonth = (start_week.replace(day=1))  # get start date of month
    enddateOfmonth = datetime.date(end_week.year + end_week.month // 12,
                                   end_week.month % 12 + 1, 1) - datetime.timedelta(1)  # get end date of month
    enddateOfyear = (start_week.replace(day=31, month=12))
    #next_three_month = start_week+datetime.timedelta(6*365/12)
    tasksInmonth_temp = models.TasksTracking.objects.filter(stopdate__range=[start_week, enddateOfyear]).filter(member=user_id)
    # get task in query time
    tasksInmonth = list()
    for t in tasksInmonth_temp:
        if t.startdate <= enddateOfmonth:
            tasksInmonth.append(t)

    block_data = models.BlockData.objects.filter(member=user_id).filter(month__range=[startdateOfmonth, enddateOfmonth])
    month_blocked = list()
    for bd in block_data:
        if bd.status:
            month_blocked.append(str(bd.month.month))
    print(month_blocked)

    context = {
        'userID': user_id,
        'task': tasks,
        'efforts_dict': efforts_dict,
        #'tasks_test': tasks_test,
        'startdate': start_week,
        'enddate': end_week,
        'taskList': tasksInmonth,
        'sumeffort': sumeffort,
        'block_data': month_blocked,
        'sum_tc': sum_tc,
        'sum_eff': sum_eff,
        'pys': pys,
    }
    return render(request, "productivity_index.html", context)


def tasks_tracking(request):
    user_id = User.objects.get(username=request.user)
    if request.is_ajax():
        if 'add_new_task' in request.POST:
            category = models.TaskCategory.objects.get(name=request.POST.get('Task_Categories'))
            update_task = models.TasksTracking(
                member=user_id,
                categories=category,
                taskName=request.POST.get('new_task'),
                effort_est=request.POST.get('efforts'),
                startdate=request.POST.get('start_date'),
                stopdate=request.POST.get('end_date'),
                status=False,
                modify_status=False
            )
            update_task.save()
            contain = {
                'success': True,
            }
            return JsonResponse(contain)
    elif request.method == 'POST':
        if 'remove_task' in request.POST:
            models.TasksTracking.objects.filter(id=request.POST['remove_task']).delete()
            selecteddate = request.POST['startDate'].replace(' ', '_')
            date_contain = {
                'month': selecteddate,
            }
            base_url = reverse('tasks_tracking')
            query_string = urlencode(date_contain)
            url = '{}?{}'.format(base_url, query_string)
            return HttpResponseRedirect(url)

        if 'edit_task' in request.POST:
            category = models.TaskCategory.objects.get(name=request.POST['Task_Categories'])
            if models.TasksTracking.objects.get(id=request.POST['edit_task']).status:
                m_status = True
            else:
                m_status = False

            models.TasksTracking.objects.filter(id=request.POST['edit_task']).update(
                    categories=category,
                    taskName=request.POST['new_task'],
                    effort_est=request.POST['efforts'],
                    startdate=request.POST['start_date'],
                    stopdate=request.POST['end_date'],
                    modify_status=m_status,
                )
            selecteddate = request.POST['startDate'].replace(' ', '_')
            date_contain = {
                'month': selecteddate,
            }
            base_url = reverse('tasks_tracking',)
            query_string = urlencode(date_contain)
            url = '{}?{}'.format(base_url, query_string)
            return HttpResponseRedirect(url)

        if 'queryMonth' in request.POST:
            # startDate = datet.strptime(request.POST['startDate'], '%B %Y')
            selecteddate = request.POST['startDate'].replace(' ', '_')
            date_contain = {
                'month': selecteddate,
            }
            base_url = reverse('tasks_tracking')
            query_string = urlencode(date_contain)
            url = '{}?{}'.format(base_url, query_string)
            return HttpResponseRedirect(url)

    if 'month' in request.GET:
        selectdate = datet.strptime(request.GET.get('month'), '%B_%Y')
    else:
        selectdate = datetime.date.today()

    startdateOfmonth = (selectdate.replace(day=1))  # get start date of month
    enddateOfmonth = datetime.date(selectdate.year + selectdate.month // 12,
                                   selectdate.month % 12 + 1, 1) - datetime.timedelta(1)  # get end date of month
    enddateOfyear = (selectdate.replace(day=31, month=12))

    tasksInmonth_temp = models.TasksTracking.objects.filter(stopdate__range=[startdateOfmonth, enddateOfyear]).filter(member=user_id)
    tasksInmonth = list()
    for t in tasksInmonth_temp:
        if t.startdate <= enddateOfmonth:
            tasksInmonth.append(t)
    # get months were blocked
    block_data = models.BlockData.objects.filter(member=user_id).filter(month__range=[startdateOfmonth, enddateOfmonth])
    month_blocked = list()
    for bd in block_data:
        if bd.status:
            month_blocked.append(str(bd.month.month))
    # --------------------------

    taskcategory = models.TaskCategory.objects.all()
    if not taskcategory:
        print('test category!!!!!!!!')
        categories = [
            'Test_Spec',
            'Test_Spec_Review',
            'Test_Auto',
            'Test_Auto_Review',
            'SW_execution',
            'Project_task_activities',
            'Project_misc',
            'Non-Project'
        ]
        for t in categories:
            category = models.TaskCategory(name=t)
            category.save()
            del category

    # add date for block data
    if tasksInmonth and not models.BlockData.objects.filter(month=startdateOfmonth).filter(member=user_id):
        BlockData = models.BlockData(
            month=startdateOfmonth,
            member=user_id,
            status=False
        )
        BlockData.save()
        del BlockData
    # end add date for block data

    contain = {
        'taskcategory': taskcategory,
        'taskInmonth': tasksInmonth,
        'selectDate': selectdate,
        'block_data': month_blocked,
    }
    return render(request, "tasks_tracking.html", contain)


def about(request):
    return render(request, "about.html", {})





