from django.db import models

class Role(models.Model):
    name = models.CharField(verbose_name='角色',max_length=32)
    def __str__(self):
        return self.name

class UserGroup(models.Model):
    title = models.CharField(verbose_name='组名',max_length=32)
    def __str__(self):
        return self.title

class UserInof(models.Model):
    user = models.CharField(verbose_name='用户名',max_length=32)
    email = models.CharField(verbose_name='邮箱',max_length=32)
    ug = models.ForeignKey(UserGroup,null=True,blank=True,verbose_name='用户组')
    m2m = models.ManyToManyField(Role,verbose_name='角色')

    def text_user(self):
        return self.user

    def val_user(self):
        return self.user

    def text_email(self):
        return self.email

    def val_email(self):
        return self.email