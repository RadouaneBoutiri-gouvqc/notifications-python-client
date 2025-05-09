import base64
import io
from unittest.mock import Mock

from notifications_python_client import prepare_upload
from tests.conftest import TEST_HOST


def test_get_notification_by_id(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications/123"
    rmock.request("GET", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.get_notification_by_id(123)

    assert rmock.called


def test_get_received_texts(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/received-text-messages"
    rmock.request("GET", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.get_received_texts()
    assert rmock.called


def test_get_received_texts_older_than(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/received-text-messages?older_than=older_id"
    rmock.request("GET", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.get_received_texts(older_than="older_id")
    assert rmock.called


def test_get_all_received_texts_iterator_calls_get_received_texts(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/received-text-messages"
    rmock.request("GET", endpoint, json={"status": "success"}, status_code=200)

    list(notifications_client.get_received_texts_iterator())
    assert rmock.called


def test_get_all_notifications_by_type_and_status(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications?status=status&template_type=type"
    rmock.request("GET", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.get_all_notifications("status", "type")

    assert rmock.called


def test_get_all_notifications_by_type(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications?template_type=type"
    rmock.request("GET", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.get_all_notifications(template_type="type")

    assert rmock.called


def test_get_all_notifications_by_reference(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications?reference=reference"
    rmock.request("GET", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.get_all_notifications(reference="reference")

    assert rmock.called


def test_get_all_notifications_by_older_than(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications?older_than=older_than"
    rmock.request("GET", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.get_all_notifications(older_than="older_than")

    assert rmock.called


def test_get_all_notifications_by_status(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications?status=status"
    rmock.request("GET", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.get_all_notifications(status="status")

    assert rmock.called


def test_get_all_notifications_including_jobs(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications?include_jobs=true"
    rmock.request("GET", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.get_all_notifications(include_jobs=True)

    assert rmock.called


def test_get_all_notifications(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications"
    rmock.request("GET", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.get_all_notifications()

    assert rmock.called


def test_create_sms_notification(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications/sms"
    rmock.request("POST", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.send_sms_notification(phone_number="07700 900000", template_id="456")

    assert rmock.last_request.json() == {"template_id": "456", "phone_number": "07700 900000"}


def test_create_sms_notification_with_personalisation(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications/sms"
    rmock.request("POST", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.send_sms_notification(
        phone_number="07700 900000", template_id="456", personalisation={"name": "chris"}
    )

    assert rmock.last_request.json() == {
        "template_id": "456",
        "phone_number": "07700 900000",
        "personalisation": {"name": "chris"},
    }


def test_create_sms_notification_with_sms_sender_id(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications/sms"
    rmock.request("POST", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.send_sms_notification(phone_number="07700 900000", template_id="456", sms_sender_id="789")

    assert rmock.last_request.json() == {"template_id": "456", "phone_number": "07700 900000", "sms_sender_id": "789"}


def test_create_email_notification(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications/email"
    rmock.request("POST", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.send_email_notification(email_address="to@example.com", template_id="456")

    assert rmock.last_request.json() == {"template_id": "456", "email_address": "to@example.com"}


def test_create_email_notification_with_email_reply_to_id(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications/email"
    rmock.request("POST", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.send_email_notification(
        email_address="to@example.com", template_id="456", email_reply_to_id="789"
    )

    assert rmock.last_request.json() == {
        "template_id": "456",
        "email_address": "to@example.com",
        "email_reply_to_id": "789",
    }


def test_create_email_notification_with_personalisation(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications/email"
    rmock.request("POST", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.send_email_notification(
        email_address="to@example.com", template_id="456", personalisation={"name": "chris"}
    )

    assert rmock.last_request.json() == {
        "template_id": "456",
        "email_address": "to@example.com",
        "personalisation": {"name": "chris"},
    }


def test_create_email_notification_with_one_click_unsubscribe_url(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications/email"
    rmock.request("POST", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.send_email_notification(
        email_address="to@example.com",
        template_id="456",
        personalisation={"name": "Namey"},
        one_click_unsubscribe_url="https://unsubscribelink.com/unsubscribe",
    )

    assert rmock.last_request.json() == {
        "template_id": "456",
        "email_address": "to@example.com",
        "personalisation": {"name": "Namey"},
        "one_click_unsubscribe_url": "https://unsubscribelink.com/unsubscribe",
    }


def test_create_email_notification_with_document_stream_upload(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications/email"
    rmock.request("POST", endpoint, json={"status": "success"}, status_code=200)

    if hasattr(io, "BytesIO"):
        mock_file = io.BytesIO(b"file-contents")
    else:
        mock_file = io.StringIO("file-contents")

    notifications_client.send_email_notification(
        email_address="to@example.com",
        template_id="456",
        personalisation={"name": "chris", "doc": prepare_upload(mock_file)},
    )

    assert rmock.last_request.json() == {
        "template_id": "456",
        "email_address": "to@example.com",
        "personalisation": {
            "name": "chris",
            "doc": {
                "file": "ZmlsZS1jb250ZW50cw==",
                "filename": None,
                "confirm_email_before_download": None,
                "retention_period": None,
            },
        },
    }


def test_create_email_notification_with_document_file_upload(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications/email"
    rmock.request("POST", endpoint, json={"status": "success"}, status_code=200)

    with open("tests/test_files/test.pdf", "rb") as f:
        notifications_client.send_email_notification(
            email_address="to@example.com",
            template_id="456",
            personalisation={"name": "chris", "doc": prepare_upload(f)},
        )

    assert rmock.last_request.json() == {
        "template_id": "456",
        "email_address": "to@example.com",
        "personalisation": {
            "name": "chris",
            "doc": {
                "file": "JVBERi0xLjUgdGVzdA0K",
                "filename": None,
                "confirm_email_before_download": None,
                "retention_period": None,
            },
        },
    }


def test_create_email_notification_with_csv_file_upload(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications/email"
    rmock.request("POST", endpoint, json={"status": "success"}, status_code=200)

    with open("tests/test_files/test.csv", "rb") as f:
        notifications_client.send_email_notification(
            email_address="to@example.com",
            template_id="456",
            personalisation={"name": "chris", "doc": prepare_upload(f, filename="file.csv")},
        )

    assert rmock.last_request.json() == {
        "template_id": "456",
        "email_address": "to@example.com",
        "personalisation": {
            "name": "chris",
            "doc": {
                "file": "VGhpcyBpcyBhIGNzdiwNCg==",
                "filename": "file.csv",
                "confirm_email_before_download": None,
                "retention_period": None,
            },
        },
    }


def test_create_letter_notification(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications/letter"
    rmock.request("POST", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.send_letter_notification(
        template_id="456", personalisation={"address_line_1": "Foo", "address_line_2": "Bar", "postcode": "SW1 1AA"}
    )

    assert rmock.last_request.json() == {
        "template_id": "456",
        "personalisation": {"address_line_1": "Foo", "address_line_2": "Bar", "postcode": "SW1 1AA"},
    }


def test_create_letter_notification_with_reference(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications/letter"
    rmock.request("POST", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.send_letter_notification(
        template_id="456",
        personalisation={"address_line_1": "Foo", "address_line_2": "Bar", "postcode": "SW1 1AA"},
        reference="Baz",
    )

    assert rmock.last_request.json() == {
        "template_id": "456",
        "personalisation": {"address_line_1": "Foo", "address_line_2": "Bar", "postcode": "SW1 1AA"},
        "reference": "Baz",
    }


def test_send_precompiled_letter_notification(notifications_client, rmock, mocker):
    endpoint = f"{TEST_HOST}/v2/notifications/letter"
    rmock.request("POST", endpoint, json={"status": "success"}, status_code=200)
    mock_file = Mock(
        read=Mock(return_value=b"file_contents"),
    )

    notifications_client.send_precompiled_letter_notification(reference="Baz", pdf_file=mock_file)

    assert rmock.last_request.json() == {
        "reference": "Baz",
        "content": base64.b64encode(b"file_contents").decode("utf-8"),
    }


def test_send_precompiled_letter_notification_sets_postage(notifications_client, rmock, mocker):
    endpoint = f"{TEST_HOST}/v2/notifications/letter"
    rmock.request("POST", endpoint, json={"status": "success"}, status_code=200)
    mock_file = Mock(
        read=Mock(return_value=b"file_contents"),
    )

    notifications_client.send_precompiled_letter_notification(reference="Baz", pdf_file=mock_file, postage="first")

    assert rmock.last_request.json() == {
        "reference": "Baz",
        "content": base64.b64encode(b"file_contents").decode("utf-8"),
        "postage": "first",
    }


def test_get_all_notifications_iterator_calls_get_notifications(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications"
    rmock.request("GET", endpoint, json={"status": "success"}, status_code=200)

    list(notifications_client.get_all_notifications_iterator())

    assert rmock.called


def test_get_all_notifications_iterator_stops_if_empty_notification_list_returned(notifications_client, rmock):
    responses = [
        _generate_response("79f9c6ce-cd6a-4b47-a3e7-41e155f112b0", [1, 2]),
        _generate_response("3e8f2f0a-0f2b-4d1b-8a01-761f14a281bb", []),
    ]

    endpoint = f"{TEST_HOST}/v2/notifications"
    rmock.request("GET", endpoint, responses)

    list(notifications_client.get_all_notifications_iterator())
    assert rmock.call_count == 2


def test_get_all_notifications_iterator_gets_more_notifications_with_correct_id(notifications_client, rmock):
    responses = [
        _generate_response("79f9c6ce-cd6a-4b47-a3e7-41e155f112b0", [1, 2]),
        _generate_response("ea179232-3190-410d-b8ab-23dfecdd3157", [3, 4]),
        _generate_response("3e8f2f0a-0f2b-4d1b-8a01-761f14a281bb", []),
    ]

    endpoint = f"{TEST_HOST}/v2/notifications"
    rmock.request("GET", endpoint, responses)
    list(notifications_client.get_all_notifications_iterator())
    assert rmock.call_count == 3


def test_get_template(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/template/{123}"
    rmock.request("GET", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.get_template(123)

    assert rmock.called


def test_get_template_version(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/template/123/version/1"
    rmock.request("GET", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.get_template_version(123, 1)

    assert rmock.called


def test_post_template_preview(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/template/123/preview"
    rmock.request("POST", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.post_template_preview(123, personalisation={"name": "chris"})

    assert rmock.called
    assert rmock.last_request.json() == {"personalisation": {"name": "chris"}}


def test_get_all_templates(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/templates"
    rmock.request("GET", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.get_all_templates()

    assert rmock.called


def test_get_all_templates_by_type(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/templates?type=type"
    rmock.request("GET", endpoint, json={"status": "success"}, status_code=200)

    notifications_client.get_all_templates("type")

    assert rmock.called


def test_get_pdf_for_letter(notifications_client, rmock):
    endpoint = f"{TEST_HOST}/v2/notifications/123/pdf"
    rmock.request("GET", endpoint, content=b"foo", status_code=200)

    response = notifications_client.get_pdf_for_letter("123")

    assert response.read() == b"foo"

    assert rmock.called


def _generate_response(next_link_uuid, notifications: list):
    return {
        "json": {
            "notifications": notifications,
            "links": {"next": f"http://localhost:6011/v2/notifications?older_than={next_link_uuid}"},
        },
        "status_code": 200,
    }
