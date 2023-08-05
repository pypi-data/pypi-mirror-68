import datetime as dt
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from os.path import basename

from simple_salesforce import Salesforce


def login(username, password, security_token):
    return jSalesforce(
        username=username, password=password, security_token=security_token,
    )


class SalesforceError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class MissingDataError(SalesforceError):
    def __init__(self, keys, data, msg=None):
        self.data = data
        if msg is None:
            msg = f"Missing data for {keys} on the data: \n{data}"
        super().__init__(msg)


class DuplicatesError(SalesforceError):
    def __init__(self, n_items, msg=None):
        self.n_items = n_items
        if msg is None:
            msg = f"There are {n_items} duplicates in salesforce."
        super().__init__(msg)


class IncompleteObjectError(SalesforceError):
    def __init__(self, object_type, sf_id, data, msg=None):
        self.object_type = object_type
        self.sf_id = sf_id
        self.data = data
        if msg is None:
            msg = f"On the {object_type} with id {sf_id} this is missing:\n{data}"
        super().__init__(msg)


class ObjectNotFoundError(SalesforceError):
    def __init__(self, object_type, identifier, msg=None):
        self.object_type = object_type
        self.identifier = identifier
        if msg is None:
            msg = f"No {object_type} found with {identifier}"
        super().__init__(msg)


class jSalesforce(Salesforce):
    def __init__(self, username, password, security_token):
        super().__init__(username, password, security_token)
        self.username = username

    def active_users(self):
        """Returns a list salesforce users that are active, usually the active
        juniors.

        Returns a list of dictionaries. Each dict represents a user and
        has the following keys: Id, Email, isActive, FirstName,
        LastName, isActive
        """
        users = self.query(
            (
                "SELECT Id, Email, isActive, FirstName, LastName "
                "FROM User WHERE isActive=True"
            )
        )["records"]
        return users

    def user_id(self, email):
        """Returns the salesforce id from the user (usually a junior) with that
        email."""
        users = self.active_users()
        try:
            sf_id = next(user["Id"] for user in users if user["Email"] == email)
        except StopIteration:
            raise SalesforceError(f"No user with email {email} found.")
        return sf_id

    def email_from_user_name(self, name):
        """Returns the email for the salesforce user with that name."""
        users = self.active_users()
        try:
            email = next(
                user["Email"]
                for user in users
                if user["FirstName"] + " " + user["LastName"] == name
            )
        except StopIteration:
            raise SalesforceError(f"No user with name {name} found.")
        return email

    def service_id(self, project_id):
        """Returns the service id with this ActiveCollab Id."""
        query = f"SELECT Id FROM Service__c WHERE ActiveCollab_Id__c={project_id}"
        records = self.query(query)["records"]
        if len(records) == 0:
            raise ObjectNotFoundError(
                "Service", f"ActiceCollab Id equal to {project_id}"
            )
        if len(records) >= 2:
            raise DuplicatesError(
                len(records),
                msg=(
                    f"There are multiple services with ActiveCollab id {project_id}"
                    f"\n{records}"
                ),
            )
        return records[0]["Id"]

    def employee_id(self, user_id):
        """Returns employee Id with this ActiveCollab Id."""
        query = (
            f"SELECT Id, Name, Prename__c, Email__c FROM Employee__c "
            f"WHERE ActiveCollab_Id__c={user_id}"
        )
        records = self.query(query)["records"]
        if len(records) == 0:
            raise ObjectNotFoundError("Employee", f"ActiceCollab Id equal to {user_id}")
        if len(records) >= 2:
            raise DuplicatesError(
                len(records),
                msg=(
                    f"There are multiple employees with ActiveCollab id {user_id}"
                    f"\n{records}"
                ),
            )
        return records[0]["Id"]

    def hiring_id(self, employee_id, service_id):
        """Returns the hiring id for this employee on this servce."""
        query = (
            f"SELECT Id, Name, Service__c, Employee__c, Role__c, "
            f"InternalPricingPerHour__c"
            f" FROM Hiring__c WHERE Employee__c='{employee_id}' AND"
            f" Service__c='{service_id}'"
        )
        records = self.query(query)["records"]
        if len(records) == 0:
            raise ObjectNotFoundError(
                "Hiring", f"employee {employee_id} on service {service_id}"
            )
        if len(records) >= 2:
            raise DuplicatesError(
                len(records),
                msg=(
                    f"There are multiple hirings for {employee_id} on {service_id}"
                    f"\n{records}"
                ),
            )
        return records[0]["Id"]

    def create_salary(self, data):
        """Creates salary from a Series, checks data for missing or
        unallowed."""
        allowed_keys = {
            "Mitarbeiter__c",
            "Service__c",
            "Anstellung__c",
            "WorkingHours__c",
            "Expenses__c",
            "InternalPricingPerHour__c",
            "Bonus__c",
            "Type__c",
            "Leistungsjahr__c",
            "Leistungsquartal__c",
            "Leistungsperiode__c",
        }
        required_keys = {
            "Mitarbeiter__c",
            "Service__c",
            "Anstellung__c",
            "WorkingHours__c",
            "Expenses__c",
            "InternalPricingPerHour__c",
            "Type__c",
            "Leistungsjahr__c",
            "Leistungsquartal__c",
            "Leistungsperiode__c",
        }
        data = data.dropna()
        data_keys = set(data.keys())
        missing_keys = required_keys - data_keys
        if len(missing_keys) > 0:
            raise MissingDataError(missing_keys, data)

        not_allowed_keys = data_keys - allowed_keys
        data = data.drop(labels=not_allowed_keys).to_dict()

        return self.Salary__c.create(data)

    def create_invoice(self, data):
        """Creates invoice from a Series, checks data for missing or
        unallowed."""
        allowed_keys = {
            "Account__c",
            "Service__c",
            "Leistungsquartal__c",
            "PeriodStart__c",
            "PeriodEnd__c",
            "Rechnungsdatum__c",
            "Account__c",
            "TermsOfPayment__c",
            "Amount1__c",
            "VAT1__c",
            "Description1__c",
            "Currency__c",
        }
        required_keys = {
            "Account__c",
            "Service__c",
            "Leistungsquartal__c",
            "PeriodStart__c",
            "PeriodEnd__c",
            "Account__c",
            "TermsOfPayment__c",
            "Amount1__c",
            "VAT1__c",
            "Description1__c",
            "Currency__c",
        }
        data = data.dropna()
        data_keys = set(data.keys())
        missing_keys = required_keys - data_keys
        if len(missing_keys) > 0:
            raise MissingDataError(missing_keys, data)

        not_allowed_keys = data_keys - allowed_keys
        data = data.drop(labels=not_allowed_keys).to_dict()

        return self.Invoices__c.create(data)

    def create_lead(self, data):
        """Creates a Lead from a pandas Series. Checks keys and data.

        Parameters
        ----------
        data: pandas Series containing at least ['Email', 'FirstName',
        'LastName', 'Company', 'OwnerId', 'Funktion__c']

        Returns
        -------
        The result from saleselforce API

        Raises
        ------
        MissingDataError
        """
        allowed_keys = {
            "Email",
            "FirstName",
            "LastName",
            "Company",
            "Funktion__c",
            "LeadSource",
            "OwnerId",
        }
        required_keys = {
            "Email",
            "FirstName",
            "LastName",
            "Company",
            "Funktion__c",
            "OwnerId",
        }
        data = data.dropna()
        data_keys = set(data.keys())
        missing_keys = required_keys - data_keys
        if len(missing_keys) > 0:
            raise MissingDataError(missing_keys, data)

        not_allowed_keys = data_keys - allowed_keys
        data = data.drop(labels=not_allowed_keys).to_dict()

        return self.Lead.create(data)

    def lead_id_from_email(self, email):
        """Returns the salesforce Id as str or None."""
        q = f"SELECT Id FROM Lead WHERE Email='{email}' AND IsConverted=False"
        records = self.query(q)["records"]
        if len(records) == 0:
            return None
        return records[0]["Id"]

    def contact_id_from_email(self, email):
        """Returns the salesforce Id as str or None."""
        q = f"SELECT Id FROM Contact WHERE Email='{email}'"
        records = self.query(q)["records"]
        if len(records) == 0:
            return None
        return records[0]["Id"]

    def create_new_leads(self, df):
        """Creates all leads from the DataFrame.

        Parameters
        ----------
        self:
        df: pandas DataFrame with columns = [Company, FirstName, LastName,
        Funktion__c, Email, Subject, Owner Email, Sales_Aktivit_t__c,
        ActivityDate, Result]

        Returns
        -------
        DataFrame: If a new Lead got created the column "Result" contains
        the new id. It also adds the WhoId and the Type to the new Leads

        Raises
        ------
        MissingDataError
        """
        df["New Lead Id"] = ""
        df["OwnerId"] = df["Owner Email"].transform(self.user_id)

        is_not_object = (
            lambda email: self.lead_id_from_email(email) is None
            and self.contact_id_from_email(email) is None
        )

        df = df.drop_duplicates(subset=["Email"])
        no_object = df["Email"].map(is_not_object)
        df_new_leads = df[no_object]
        for row in df_new_leads.iterrows():
            data = row[1]
            print(f"Creating Lead for: {data['Email']}")
            result = self.create_lead(data)
            lead_id = result["id"]
            print(f"Created Lead with id {lead_id}")
            df.at[row[0], "New Lead Id"] = lead_id
            df.at[row[0], "Types"] = {"Lead"}
        return df

    def create_task(self, data):
        """Creates a Task based on a pandas Series. Checks keys and data.
        Parameters
        ----------
        self:
        data: pandas Series containing at least
        ['WhoId','Subject','ActivityDate','Status','OwnerId','Sales_Aktivit_t__c']

        Returns
        -------
        The result from salesforce API

        Raises
        ------
        MissingDataError
        """
        allowed_keys = {
            "WhoId",
            "WhatId",
            "Subject",
            "ActivityDate",
            "Status",
            "Description",
            "OwnerId",
            "Sales_Aktivit_t__c",
        }
        required_keys = {
            "WhoId",
            "Subject",
            "ActivityDate",
            "Status",
            "OwnerId",
            "Sales_Aktivit_t__c",
        }
        data = data.dropna()
        data_keys = set(data.keys())
        missing_keys = required_keys - data_keys
        if len(missing_keys) > 0:
            raise MissingDataError(missing_keys, data)

        not_allowed_keys = data_keys - allowed_keys
        data = data.drop(labels=not_allowed_keys).to_dict()

        return self.Task.create(data)

    def create_tasks(self, df):
        """Creates all tasks from the DataFrame.

        Parameters
        ----------
        self: Salesforce connectore from login function
        df: DataFrame containing at least the columns
        ['Email','Subject','ActivityDate','Status','Owner
        Email','Sales_Aktivit_t__c', 'Result']

        Returns
        -------
        DataFrame: the same DataFrame with the Task id added to the column "Result"

        Raises
        ------
        MissingDataError
        """
        df["New Task Id"] = ""

        df["OwnerId"] = df["Owner Email"].transform(self.user_id)

        df["LeadId"] = df["Email"].map(self.lead_id_from_email)
        df["ContactId"] = df["Email"].map(self.contact_id_from_email)
        is_lead = ~df["LeadId"].isna()
        is_contact = ~df["ContactId"].isna()
        df["WhoId"] = None
        df.loc[is_lead, "WhoId"] = df["LeadId"]
        df.loc[is_contact, "WhoId"] = df["ContactId"]

        is_object = ~df["WhoId"].isna()
        has_task = ~df["Status"].isna()

        for row in df[is_object & has_task].iterrows():
            data = row[1]
            # TODO handle exception
            print(f"Creating Task for: {data['Email']}")
            result = self.create_task(data)
            task_id = result["id"]
            print(f"Tracked Task with id {task_id}")
            df.at[row[0], "New Task Id"] = task_id
        return df

    def get_objects_created_after(self, python_dt, object_type):
        """Returns objects of specific type created by the logged in user after
        that time."""
        salesforce_dt = to_salesforce_datetime(python_dt)
        user_id = self.user_id(self.username)
        q = (
            f"SELECT Id FROM {object_type} WHERE CreatedDate > {salesforce_dt}"
            f"AND CreatedById='{user_id}'"
        )
        return self.query(q)["records"]

    def delete_object(self, salesforce_id, object_type):
        """Deletes salesforce object with that id and that type."""
        delete_function = {"Lead": self.Lead.delete, "Task": self.Task.delete}
        result = delete_function[object_type](salesforce_id)
        return result

    def delete_objects_created_after(self, python_dt, object_type, delete_many=False):
        """Deletes objects of specific type created after some time.

        Protects against mass deletions of more than 25 elements by
        default. Set delete_many=True if you want to skip that
        protection.
        """
        records = self.get_objects_created_after(python_dt, object_type)
        if len(records) > 25 and delete_many is False:
            raise DuplicatesError(
                len(records),
                msg=(
                    f"You are about to delete {records} items. If that is "
                    f"correct, call the function with delete_many=True"
                ),
            )

        for record in records:
            salesforce_id = record["Id"]
            result = self.delete_object(salesforce_id, object_type)
            # TODO: Use proper logging
            print(
                f"Deleted object with Type {object_type} and id "
                f"{salesforce_id}. Result:\n{result}"
            )
        return


def to_salesforce_datetime(python_dt):
    """Converts python datetime to the salesforce format.

    Example: 2014-11-20T14:23:44.000+0000
    """
    return python_dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+0000"


def to_python_datetime(salesforce_dt):
    """Converts salesforce datetime to a python datetime.

    Example: 2014-11-20T14:23:44.000+0000 converts to the python datetime
    """
    return dt.datetime.strptime(sf_datetime, "%Y-%m-%dT%H:%M:%S.%f+0000")


def to_date(date):
    """Convert python datetime.date to the salesforce string format, e.g.
    '2020-02-29'."""
    return date.strftime("%Y-%m-%d")


def month_name(month):
    """Returns the month name for ETH juniors Salesforce"""
    month_names = {
        1: "Januar",
        2: "Februar",
        3: "März",
        4: "April",
        5: "Mai",
        6: "Juni",
        7: "Juli",
        8: "August",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Dezember",
    }
    return month_names[month]


def quartal_name(quartal):
    """Returns the quartal name for ETH juniors Salesforce"""
    quartal_names = {
        1: "Q1",
        2: "Q2",
        3: "Q3",
        4: "Q4",
    }
    return quartal_names[quartal]


def send_mail(server, username, password, send_from, send_to, subject, html, files):
    """Sends an html email with the reply to adress = send_from.

    The send_to paramater has to be a list. You can attach files by specifying
    filenames in the parameter files. The server, username and password was
    tested for gmail.
    """
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg["From"] = send_from
    msg["To"] = COMMASPACE.join(send_to)
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject
    msg.add_header("reply-to", send_from)
    html = MIMEText(html, "html")
    msg.attach(html)

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(fil.read(), Name=basename(f))
        # After the file is closed
        part["Content-Disposition"] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    s = smtplib.SMTP(server, 587)
    s.starttls()
    s.login(username, password)
    s.sendmail(send_from, send_to, msg.as_string())
    s.quit()
