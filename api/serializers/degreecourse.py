from rest_framework import serializers
from api import models



class DegreeCourseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    brief = serializers.CharField()
    total_scholarship = serializers.IntegerField()
    mentor_compensation_bonus = serializers.IntegerField()
    period = serializers.IntegerField()

    teacher = serializers.SerializerMethodField()

    def get_teacher(self,row):
        teacher_obj_list = row.teacher.all()

        return [{'name': item.name} for item in teacher_obj_list ]

    # name = models.CharField(max_length=128, unique=True)
    # course_img = models.CharField(max_length=255, verbose_name="缩略图")
    # brief = models.TextField(verbose_name="学位课程简介", )
    # total_scholarship = models.PositiveIntegerField(verbose_name="总奖学金(贝里)", default=40000)  # 2000 2000
    # mentor_compensation_bonus = models.PositiveIntegerField(verbose_name="本课程的导师辅导费用(贝里)", default=15000)
    # period = models.PositiveIntegerField(verbose_name="建议学习周期(days)", default=150)  # 为了计算学位奖学金
    # prerequisite = models.TextField(verbose_name="课程先修要求", max_length=1024)
    # teachers = models.ManyToManyField("Teacher", verbose_name="课程讲师")