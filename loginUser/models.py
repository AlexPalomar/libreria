from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from datetime import datetime 

class ManagerUser(BaseUserManager):
    def create_user(self, identificationUser, emailUser,firstnameUser,lastnameUser,ageUser,phoneUser,password=None):
        if not emailUser:
            raise ValueError('Usuarios deben tener un correo electronico válido')
        
        user = self.model(
            identificationUser = identificationUser,
            emailUser= self.normalize_email(emailUser),
            firstnameUser = firstnameUser,
            lastnameUser = lastnameUser,
            ageUser = ageUser,
            phoneUser = phoneUser,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def update_user(self,firstnameUser,lastnameUser,ageUser,phoneUser,):
        
        user = self.model(
            firstnameUser = firstnameUser,
            lastnameUser = lastnameUser,
            ageUser = ageUser,
            phoneUser = phoneUser,
        )
        return user
        
    def create_superuser(self,identificationUser, emailUser,firstnameUser,lastnameUser,ageUser,phoneUser,password):
        user = self.create_user(
            identificationUser= identificationUser,
            emailUser= emailUser,
            firstnameUser = firstnameUser,
            lastnameUser = lastnameUser,
            ageUser = ageUser,
            phoneUser = phoneUser,
            password = password
        )
        user.adminUser = True
        user.save()
        return user


class User(AbstractBaseUser):

    identificationUser = models.IntegerField('Identificacion', default=None, unique=True, null = False)
    emailUser = models.EmailField('correo electrónico', max_length=100, unique=True) 
    firstnameUser = models.CharField('Nombre',max_length=60)
    lastnameUser = models.CharField('Apellido',max_length=60, null = True)
    ageUser = models.IntegerField('Edad', null = True)
    phoneUser = models.CharField('Telefono', null = False, max_length=15)
    appointmentUser = models.DateTimeField('Fecha de cita',default=datetime.now, blank=True)
    imageUser = models.ImageField('Imagen de perfil', upload_to='perfil/', max_length=200, blank=True, null=True)
    writerUser = models.BooleanField(default = False)
    activeUser = models.BooleanField(default = True)
    adminUser = models.BooleanField(default = False)

    # Establecer manejador del modelo (definido en el siguiente paso) objects ManejadorUsuario()
    objects = ManagerUser()
    operation = ManagerUser()

    USERNAME_FIELD = 'emailUser' #definimos el correo como el "nombre de usuario" 
    REQUIRED_FIELDS = ['identificationUser', 'firstnameUser','lastnameUser','phoneUser','ageUser'] #correo y contraseña son requeridos por defecto.

    def __str__(self):
        return f'{self.identificationUser},{self.firstnameUser},{self.lastnameUser},{self.phoneUser},{self.appointmentUser},{self.emailUser}'
    
    def has_perm(self, perm, obj=None): 
        return True
    
    def has_module_perms(self, app_Label): 
        return True
    
    
    @property
    def is_staff(self):
        return self.adminUser