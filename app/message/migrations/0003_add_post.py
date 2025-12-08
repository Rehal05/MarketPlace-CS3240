from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0002_message_image'),
        ('feedapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='feedapp.post'),
        ),
    ]
