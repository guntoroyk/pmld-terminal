from django import forms
from .models import PencatatanBus
from .models import Bus

class PencatatanBusForm(forms.ModelForm):
    class Meta:
        model = PencatatanBus
        fields = [
            'bus', 'jenis', 'penumpang_datang', 'penumpang_turun',
            'penumpang_naik', 'penumpang_berangkat', 'keterangan',
            'waktu_datang'
        ]


class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ('__all__')