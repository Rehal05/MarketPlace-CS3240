from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('delisted', 'Delisted')], default='active', help_text='Whether this post is visible in the feed or delisted by moderators.', max_length=20),
        ),
    ]
