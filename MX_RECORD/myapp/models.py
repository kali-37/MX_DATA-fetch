from django.db import models


class UnverifiedData(models.Model):
    s_no = models.IntegerField(default=1)
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    address = models.CharField(max_length=254)
    city = models.CharField(max_length=70)
    pin = models.CharField(max_length=16)
    country = models.CharField(max_length=70, default="India")
    state = models.CharField(max_length=70)
    landline_no = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=180)
    email_id = models.CharField(max_length=254)
    website = models.CharField(
        max_length=254, primary_key=True, db_collation="utf8mb4_bin"
    )

    def __str__(self):
        return self.company_name + " - " + self.website


class Domain(models.Model):
    name = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.name  #


class MXRecordAll(models.Model):
    domain = models.ForeignKey(
        Domain, on_delete=models.CASCADE, related_name="mx_records"
    )
    first_seen = models.DateField()
    last_seen = models.DateField()
    organizations = models.TextField()
    selected_month = models.CharField(max_length=70, default="")
    state = models.CharField(max_length=70, default="Delhi")
    country = models.CharField(max_length=70, default="India")

    def __str__(self):
        return f"{self.domain} ({self.first_seen} - {self.last_seen})"


class MXRecordcurrent(models.Model):
    domain = models.ForeignKey(
        Domain, on_delete=models.CASCADE, related_name="mx_records_current"
    )
    first_seen = models.DateField()
    last_seen = models.DateField()
    organizations = models.TextField()
    selected_month = models.CharField(max_length=70, default="")
    state = models.CharField(max_length=70, default="Delhi")
    country = models.CharField(max_length=70, default="India")

    def __str__(self):
        return f"{self.domain} ({self.first_seen} - {self.last_seen})"


class MailServerHistorical(models.Model):
    mx_record = models.ForeignKey(
        MXRecordAll, on_delete=models.CASCADE, related_name="mail_servers"
    )  #
    host = models.CharField(max_length=255)

    def __str__(self):
        return self.host


class MailServercurrent(models.Model):
    current_mx = models.ForeignKey(
        MXRecordcurrent, on_delete=models.CASCADE, related_name="current_mail_servers"
    )  #
    current_host = models.CharField(max_length=255)

    def __str__(self):
        return str(self.current_mx) + " - " + self.current_host


# countries :


class Country(models.Model):
    country_name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.country_name


class State(models.Model):
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="states"
    )
    state_name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return str(self.country) + "-" + str(self.state_name)
