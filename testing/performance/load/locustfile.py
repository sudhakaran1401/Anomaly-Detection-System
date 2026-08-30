from locust import HttpUser, task, between
from locust.exception import StopUser
import io
import random


# ============================================================
# CONFIGURATION
# ============================================================

USERNAME = "e2e_test_user"
PASSWORD = "E2eTest@12345"

# Default API host.
# You can override it from the Locust UI.
DEFAULT_HOST = "http://127.0.0.1:8000"


# ============================================================
# TEST DATA
# ============================================================

# Unlabelled dataset for anomaly detection.
#
# Columns must be numeric because the anomaly service processes
# the dataset through the configured ML models.
#
# A few deliberately large values are included as potential
# outliers.
ANOMALY_CSV = """feature_1,feature_2,feature_3
10,20,100
11,21,101
12,22,102
13,23,103
14,24,104
15,25,105
16,26,106
17,27,107
18,28,108
19,29,109
20,30,110
21,31,111
22,32,112
23,33,113
24,34,114
25,35,115
26,36,116
27,37,117
28,38,118
29,39,119
30,40,120
31,41,121
32,42,122
33,43,123
34,44,124
35,45,125
36,46,126
37,47,127
38,48,128
39,49,129
40,50,130
41,51,131
42,52,132
43,53,133
44,54,134
45,55,135
46,56,136
47,57,137
48,58,138
49,59,139
50,60,140
51,61,141
52,62,142
53,63,143
54,64,144
55,65,145
56,66,146
57,67,147
58,68,148
59,69,149
60,70,150
61,71,151
62,72,152
63,73,153
64,74,154
65,75,155
66,76,156
67,77,157
68,78,158
69,79,159
70,80,160
71,81,161
72,82,162
73,83,163
74,84,164
75,85,165
76,86,166
77,87,167
78,88,168
79,89,169
80,90,170
81,91,171
82,92,172
83,93,173
84,94,174
85,95,175
86,96,176
87,97,177
88,98,178
89,99,179
90,100,180
91,101,181
92,102,182
93,103,183
94,104,184
95,105,185
96,106,186
97,107,187
98,108,188
99,109,189
100,110,190
250,350,1000
300,450,1500
350,550,2000
400,650,2500
"""


# Labelled dataset for classification.
#
# The application uses the classification API independently
# from the anomaly API.
#
# "Target" is used because the backend classification result
# model stores target_column as "Target".
CLASSIFICATION_CSV = """feature_1,feature_2,feature_3,Target
10,20,100,0
11,21,101,0
12,22,102,0
13,23,103,0
14,24,104,0
15,25,105,0
16,26,106,0
17,27,107,0
18,28,108,0
19,29,109,0
20,30,110,0
21,31,111,0
22,32,112,0
23,33,113,0
24,34,114,0
25,35,115,0
26,36,116,0
27,37,117,0
28,38,118,0
29,39,119,0
30,40,120,0
31,41,121,0
32,42,122,0
33,43,123,0
34,44,124,0
35,45,125,0
36,46,126,0
37,47,127,0
38,48,128,0
39,49,129,0
40,50,130,0
41,51,131,0
42,52,132,0
43,53,133,0
44,54,134,0
45,55,135,0
46,56,136,0
47,57,137,0
48,58,138,0
49,59,139,0
50,60,140,0
51,61,141,0
52,62,142,0
53,63,143,0
54,64,144,0
55,65,145,0
56,66,146,0
57,67,147,0
58,68,148,0
59,69,149,0
60,70,150,0
61,71,151,0
62,72,152,0
63,73,153,0
64,74,154,0
65,75,155,0
66,76,156,0
67,77,157,0
68,78,158,0
69,79,159,0
70,80,160,0
71,81,161,0
72,82,162,0
73,83,163,0
74,84,164,0
75,85,165,0
76,86,166,0
77,87,167,0
78,88,168,0
79,89,169,0
80,90,170,0
81,91,171,0
82,92,172,0
83,93,173,0
84,94,174,0
85,95,175,0
86,96,176,0
87,97,177,0
88,98,178,0
89,99,179,0
90,100,180,0
91,101,181,0
92,102,182,0
93,103,183,0
94,104,184,0
95,105,185,0
96,106,186,0
97,107,187,0
98,108,188,0
99,109,189,0
100,110,190,1
101,111,191,1
102,112,192,1
103,113,193,1
104,114,194,1
105,115,195,1
106,116,196,1
107,117,197,1
108,118,198,1
109,119,199,1
110,120,200,1
111,121,201,1
112,122,202,1
113,123,203,1
114,124,204,1
115,125,205,1
116,126,206,1
117,127,207,1
118,128,208,1
119,129,209,1
120,130,210,1
121,131,211,1
122,132,212,1
123,133,213,1
124,134,214,1
125,135,215,1
126,136,216,1
127,137,217,1
128,138,218,1
129,139,219,1
130,140,220,1
131,141,221,1
132,142,222,1
133,143,223,1
134,144,224,1
135,145,225,1
136,146,226,1
137,147,227,1
138,148,228,1
139,149,229,1
140,150,230,1
141,151,231,1
142,152,232,1
143,153,233,1
144,154,234,1
145,155,235,1
146,156,236,1
147,157,237,1
148,158,238,1
149,159,239,1
150,160,240,1
"""


# ============================================================
# LOCUST USER
# ============================================================

class AnomalyDetectionUser(HttpUser):

    wait_time = between(1, 3)

    # If Locust is started without --host, this is used.
    host = DEFAULT_HOST

    # Runtime state for this virtual user.
    access_token = None
    refresh_token = None
    anomaly_result_id = None
    classification_result_id = None

    # --------------------------------------------------------
    # AUTHENTICATION
    # --------------------------------------------------------

    def on_start(self):
        """
        Runs once when a Locust virtual user starts.

        The application uses JWT authentication through:

            POST /api/token/

        The actual Django project exposes this endpoint.
        """

        response = self.client.post(
            "/api/token/",
            json={
                "username": USERNAME,
                "password": PASSWORD,
            },
            name="POST /api/token/"
        )

        if response.status_code != 200:
            print(
                "\nLOGIN FAILED"
                f"\nStatus: {response.status_code}"
                f"\nResponse: {response.text}\n"
            )

            raise StopUser()

        try:
            data = response.json()

            self.access_token = data["access"]
            self.refresh_token = data.get("refresh")

        except Exception as exc:
            print(
                "\nINVALID TOKEN RESPONSE"
                f"\nResponse: {response.text}"
                f"\nError: {exc}\n"
            )

            raise StopUser()

    # --------------------------------------------------------
    # HEADERS
    # --------------------------------------------------------

    def auth_headers(self):
        """
        Return the Authorization header expected by DRF
        SimpleJWT.
        """

        return {
            "Authorization": f"Bearer {self.access_token}",
        }

    # --------------------------------------------------------
    # FILE HELPERS
    # --------------------------------------------------------

    def anomaly_file(self):
        """
        Return a fresh in-memory CSV file.

        A fresh BytesIO object is used for every request because
        Locust/requests consumes the file stream.
        """

        return {
            "file": (
                "locust_anomaly.csv",
                io.BytesIO(
                    ANOMALY_CSV.encode("utf-8")
                ),
                "text/csv",
            )
        }

    def classification_file(self):
        """
        Return a fresh labelled CSV file.
        """

        return {
            "file": (
                "locust_classification.csv",
                io.BytesIO(
                    CLASSIFICATION_CSV.encode("utf-8")
                ),
                "text/csv",
            )
        }

    # ========================================================
    # BASIC API TESTS
    # ========================================================

    @task(1)
    def get_anomaly_results(self):
        """
        GET /api/anomaly/results/

        Tests the authenticated anomaly-result endpoint.
        """

        response = self.client.get(
            "/api/anomaly/results/",
            headers=self.auth_headers(),
            name="GET /api/anomaly/results/"
        )

        if response.status_code not in (200, 204):
            response.failure(
                f"Unexpected status {response.status_code}"
            )

    @task(1)
    def get_detection_history(self):
        """
        GET /api/anomaly/history/
        """

        response = self.client.get(
            "/api/anomaly/history/",
            headers=self.auth_headers(),
            name="GET /api/anomaly/history/"
        )

        if response.status_code != 200:
            response.failure(
                f"Unexpected status {response.status_code}"
            )

    @task(1)
    def get_classification_results(self):
        """
        GET /api/classification/results/
        """

        response = self.client.get(
            "/api/classification/results/",
            headers=self.auth_headers(),
            name="GET /api/classification/results/"
        )

        if response.status_code != 200:
            response.failure(
                f"Unexpected status {response.status_code}"
            )

    # ========================================================
    # ANOMALY DETECTION
    # ========================================================

    @task(4)
    def anomaly_isolation_forest(self):
        """
        Main anomaly-detection load test.

        Actual API endpoint:

            POST /api/anomaly/analyze/

        Actual model value:

            isolation_forest
        """

        files = self.anomaly_file()

        data = {
            "model_name": "isolation_forest",
            "scaler_type": random.choice(
                [
                    "standard",
                    "minmax",
                    "robust",
                ]
            ),
            "contamination": random.choice(
                [
                    "0.01",
                    "0.02",
                    "0.05",
                    "0.10",
                ]
            ),
        }

        with self.client.post(
            "/api/anomaly/analyze/",
            headers=self.auth_headers(),
            files=files,
            data=data,
            name="POST /api/anomaly/analyze/ [Isolation Forest]",
            catch_response=True,
        ) as response:

            if response.status_code != 200:
                response.failure(
                    f"Anomaly analysis failed: "
                    f"{response.status_code} "
                    f"{response.text[:500]}"
                )
                return

            try:
                body = response.json()

                if not body.get("success"):
                    response.failure(
                        "API returned success=false"
                    )
                    return

                if "data" not in body:
                    response.failure(
                        "Response does not contain data"
                    )
                    return

                # Store result ID if returned by the API.
                data_result = body.get("data", {})

                result_id = (
                    data_result.get("id")
                    or data_result.get("result_id")
                )

                if result_id:
                    self.anomaly_result_id = result_id

            except Exception as exc:
                response.failure(
                    f"Invalid JSON response: {exc}"
                )

    @task(1)
    def anomaly_lof(self):
        """
        Local Outlier Factor.

        Actual model value from the application:

            lof
        """

        with self.client.post(
            "/api/anomaly/analyze/",
            headers=self.auth_headers(),
            files=self.anomaly_file(),
            data={
                "model_name": "lof",
                "scaler_type": "standard",
                "contamination": "0.05",
            },
            name="POST /api/anomaly/analyze/ [LOF]",
            catch_response=True,
        ) as response:

            if response.status_code != 200:
                response.failure(
                    f"LOF failed: {response.status_code}"
                )

    @task(1)
    def anomaly_svm(self):
        """
        One-Class SVM.

        IMPORTANT:
        The actual frontend constant is:

            svm

        not:

            one_class_svm
        """

        with self.client.post(
            "/api/anomaly/analyze/",
            headers=self.auth_headers(),
            files=self.anomaly_file(),
            data={
                "model_name": "svm",
                "scaler_type": "standard",
                "contamination": "0.05",
            },
            name="POST /api/anomaly/analyze/ [SVM]",
            catch_response=True,
        ) as response:

            if response.status_code != 200:
                response.failure(
                    f"SVM failed: {response.status_code}"
                )

    @task(1)
    def anomaly_dbscan(self):
        """
        DBSCAN anomaly detection.
        """

        with self.client.post(
            "/api/anomaly/analyze/",
            headers=self.auth_headers(),
            files=self.anomaly_file(),
            data={
                "model_name": "dbscan",
                "scaler_type": "standard",
                "contamination": "0.05",
            },
            name="POST /api/anomaly/analyze/ [DBSCAN]",
            catch_response=True,
        ) as response:

            if response.status_code != 200:
                response.failure(
                    f"DBSCAN failed: {response.status_code}"
                )

    # ========================================================
    # ANOMALY HISTORY
    # ========================================================

    @task(2)
    def get_anomaly_history(self):
        """
        Retrieve authenticated detection history.
        """

        response = self.client.get(
            "/api/anomaly/history/",
            headers=self.auth_headers(),
            name="GET /api/anomaly/history/"
        )

        if response.status_code != 200:
            response.failure(
                f"History failed: {response.status_code}"
            )

    # ========================================================
    # ANOMALY CSV DOWNLOAD
    # ========================================================

    @task(1)
    def download_anomaly_csv(self):
        """
        Download processed anomaly CSV.

        Actual endpoint:

            GET /api/anomaly/download/csv/
        """

        with self.client.get(
            "/api/anomaly/download/csv/",
            headers=self.auth_headers(),
            params={
                "filter": random.choice(
                    [
                        "all",
                        "anomaly",
                        "normal",
                    ]
                )
            },
            name="GET /api/anomaly/download/csv/",
            catch_response=True,
        ) as response:

            # 404 is possible when this virtual user has not yet
            # created a processed result.
            if response.status_code not in (
                200,
                404,
            ):
                response.failure(
                    f"CSV download failed: "
                    f"{response.status_code}"
                )

    # ========================================================
    # ANOMALY PDF DOWNLOAD
    # ========================================================

    @task(1)
    def download_anomaly_pdf(self):
        """
        Download anomaly PDF.

        Actual endpoint:

            GET /api/anomaly/download/pdf/
        """

        params = {
            "filename": "locust_anomaly.csv",
            "model_name": "isolation_forest",
            "scaler_type": "standard",
            "contamination": "0.05",
            "filter": "all",
        }

        with self.client.get(
            "/api/anomaly/download/pdf/",
            headers=self.auth_headers(),
            params=params,
            name="GET /api/anomaly/download/pdf/",
            catch_response=True,
        ) as response:

            if response.status_code not in (
                200,
                404,
            ):
                response.failure(
                    f"PDF download failed: "
                    f"{response.status_code}"
                )

    # ========================================================
    # CLASSIFICATION
    # ========================================================

    @task(2)
    def classification_random_forest(self):
        """
        Classification API load test.

        Actual endpoint:

            POST /api/classification/classify/

        Actual model:

            random_forest
        """

        with self.client.post(
            "/api/classification/classify/",
            headers=self.auth_headers(),
            files=self.classification_file(),
            data={
                "model_name": "random_forest",
                "scaler_type": "standard",
            },
            name="POST /api/classification/classify/ [Random Forest]",
            catch_response=True,
        ) as response:

            if response.status_code != 200:
                response.failure(
                    f"Classification failed: "
                    f"{response.status_code} "
                    f"{response.text[:500]}"
                )
                return

            try:
                body = response.json()

                if not body.get("success"):
                    response.failure(
                        "Classification returned success=false"
                    )
                    return

                result = body.get("result")

                if result:
                    self.classification_result_id = (
                        result.get("id")
                    )

            except Exception as exc:
                response.failure(
                    f"Invalid classification JSON: {exc}"
                )

    # ========================================================
    # CLASSIFICATION RESULT DETAIL
    # ========================================================

    @task(1)
    def get_classification_result(self):
        """
        GET /api/classification/results/

        First retrieves available results and then, when an ID
        exists, retrieves the detail endpoint.
        """

        response = self.client.get(
            "/api/classification/results/",
            headers=self.auth_headers(),
            name="GET /api/classification/results/"
        )

        if response.status_code != 200:
            response.failure(
                f"Classification results failed: "
                f"{response.status_code}"
            )
            return

        try:
            body = response.json()

            results = body.get(
                "results",
                []
            )

            if not results:
                return

            result_id = results[0].get("id")

            if not result_id:
                return

            self.classification_result_id = result_id

            detail = self.client.get(
                f"/api/classification/results/{result_id}/",
                headers=self.auth_headers(),
                name="GET /api/classification/results/{id}/"
            )

            if detail.status_code != 200:
                detail.failure(
                    f"Classification detail failed: "
                    f"{detail.status_code}"
                )

        except Exception as exc:
            response.failure(
                f"Invalid classification result response: {exc}"
            )

    # ========================================================
    # CLASSIFICATION PDF
    # ========================================================

    @task(1)
    def download_classification_pdf(self):
        """
        Download classification PDF for the most recent
        classification result belonging to this user.
        """

        if not self.classification_result_id:
            return

        result_id = self.classification_result_id

        with self.client.get(
            f"/api/classification/results/"
            f"{result_id}/download/pdf/",
            headers=self.auth_headers(),
            name="GET /api/classification/results/{id}/download/pdf/",
            catch_response=True,
        ) as response:

            if response.status_code != 200:
                response.failure(
                    f"Classification PDF failed: "
                    f"{response.status_code}"
                )

    # ========================================================
    # REFRESH TOKEN
    # ========================================================

    @task(1)
    def refresh_access_token(self):
        """
        Exercise the JWT refresh endpoint.

        Actual endpoint:

            POST /api/token/refresh/
        """

        if not self.refresh_token:
            return

        response = self.client.post(
            "/api/token/refresh/",
            json={
                "refresh": self.refresh_token,
            },
            name="POST /api/token/refresh/"
        )

        if response.status_code != 200:
            response.failure(
                f"Token refresh failed: "
                f"{response.status_code}"
            )
            return

        try:
            body = response.json()

            new_access = body.get(
                "access"
            )

            if new_access:
                self.access_token = new_access

        except Exception as exc:
            response.failure(
                f"Invalid refresh response: {exc}"
            )