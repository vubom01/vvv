from datetime import date

from app.db.base import mysql
from app.schemas.sche_work_schedule import ConfirmWorkSchedule, WorkSchedule


class WorkScheduleService(object):

    @staticmethod
    def register_work_schedule(user_id: int, data: WorkSchedule):
        cursor = mysql.cursor()
        query = 'insert into work_schedule (user_id, working_day, working_shift) values (%s, %s, %s)'
        cursor.execute(query, (user_id, data.working_day, data.working_shift))
        mysql.commit()

    @staticmethod
    def is_exist_work_schedule(user_id: int, working_day: date):
        cursor = mysql.cursor()
        query = 'select * from work_schedule where user_id = %s and working_day = %s'
        cursor.execute(query, (user_id, working_day,))
        res = cursor.fetchone()
        if not res:
            return None
        return res

    @staticmethod
    def confirm_work_schedule(user_id: int, data: ConfirmWorkSchedule):
        cursor = mysql.cursor()
        query = 'UPDATE work_schedule SET status = %s where user_id = %s and working_day = %s'
        cursor.execute(query, (data.status, user_id, data.working_day))
        mysql.commit()

    @staticmethod
    def delete_work_schedule(user_id: int, working_day: date):
        cursor = mysql.cursor()
        query = 'delete from work_schedule where user_id = %s and working_day = %s'
        cursor.execute(query, (user_id, working_day))
        mysql.commit()

    @staticmethod
    def update_work_schedule(user_id: int, data: WorkSchedule):
        cursor = mysql.cursor()
        query = 'update work_schedule set working_shift = %s where user_id = %s and working_day = %s'
        cursor.execute(query, (data.working_shift, user_id, data.working_day))
        mysql.commit()

    @staticmethod
    def get_list_work_schedule_by_user_id(user_id: int, start_at: date, end_at: date):
        if start_at is None:
            start_at = '1000-01-01'
        if end_at is None:
            end_at = '3000_12_31'
        cursor = mysql.cursor()
        query = 'select working_day, working_shift, status from work_schedule where user_id = %s ' \
                'and working_day between %s and %s'
        cursor.execute(query, (user_id, start_at, end_at))
        work_schedule = cursor.fetchall()
        return work_schedule
