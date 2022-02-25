import django.dispatch

save_done = django.dispatch.Signal()


class SaveDoneSignalMixin:

    def save(self, *args, **kwargs):
        old = self.__class__.objects.filter(pk=self.pk).first()
        super(SaveDoneSignalMixin, self).save()
        new = self.__class__.objects.filter(pk=self.pk).first()
        save_done.send(sender=self.__class__, old=old, new=new)
