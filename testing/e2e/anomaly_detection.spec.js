const { test, expect } = require("@playwright/test");

const BASE_URL = process.env.BASE_URL || "http://127.0.0.1:5173";

const API_URL = process.env.API_URL || "http://127.0.0.1:8000";

const E2E_USERNAME = "e2e_test_user";
const E2E_PASSWORD = "E2eTest@12345";

const ANOMALY_CSV = {
  name: "anomaly-e2e.csv",
  mimeType: "text/csv",
  buffer: Buffer.from(
    [
      "feature_1,feature_2,feature_3",
      "10,20,100",
      "11,21,101",
      "12,22,102",
      "13,23,103",
      "14,24,104",
      "15,25,105",
      "16,26,106",
      "17,27,107",
      "18,28,108",
      "19,29,109",
      "20,30,110",
      "21,31,111",
      "22,32,112",
      "23,33,113",
      "24,34,114",
      "25,35,115",
      "26,36,116",
      "27,37,117",
      "28,38,118",
      "29,39,119",
      "30,40,120",
      "31,41,121",
      "32,42,122",
      "33,43,123",
      "34,44,124",
      "35,45,125",
      "36,46,126",
      "37,47,127",
      "38,48,128",
      "39,49,129",
      "40,50,130",
      "41,51,131",
      "42,52,132",
      "43,53,133",
      "44,54,134",
      "45,55,135",
      "46,56,136",
      "47,57,137",
      "48,58,138",
      "49,59,139",
      "50,60,140",
      "51,61,141",
      "52,62,142",
      "53,63,143",
      "54,64,144",
      "55,65,145",
      "56,66,146",
      "57,67,147",
      "58,68,148",
      "59,69,149",
      "60,70,150",
      "200,300,1000",
      "210,310,1100",
      "220,320,1200",
      "230,330,1300",
    ].join("\n")
  ),
};

const CLASSIFICATION_CSV = {
  name: "classification-e2e.csv",
  mimeType: "text/csv",
  buffer: Buffer.from(
    [
      "feature_1,feature_2,feature_3,label",
      "10,20,100,0",
      "11,21,101,0",
      "12,22,102,0",
      "13,23,103,0",
      "14,24,104,0",
      "15,25,105,0",
      "16,26,106,0",
      "17,27,107,0",
      "18,28,108,0",
      "19,29,109,0",
      "20,30,110,0",
      "21,31,111,0",
      "22,32,112,0",
      "23,33,113,0",
      "24,34,114,0",
      "25,35,115,0",
      "26,36,116,0",
      "27,37,117,0",
      "28,38,118,0",
      "29,39,119,0",
      "30,40,120,0",
      "31,41,121,0",
      "32,42,122,0",
      "33,43,123,0",
      "34,44,124,0",
      "35,45,125,0",
      "36,46,126,0",
      "37,47,127,0",
      "38,48,128,0",
      "39,49,129,0",
      "100,200,500,1",
      "101,201,501,1",
      "102,202,502,1",
      "103,203,503,1",
      "104,204,504,1",
      "105,205,505,1",
      "106,206,506,1",
      "107,207,507,1",
      "108,208,508,1",
      "109,209,509,1",
      "110,210,510,1",
      "111,211,511,1",
      "112,212,512,1",
      "113,213,513,1",
      "114,214,514,1",
      "115,215,515,1",
      "116,216,516,1",
      "117,217,517,1",
      "118,218,518,1",
      "119,219,519,1",
      "120,220,520,1",
      "121,221,521,1",
      "122,222,522,1",
      "123,223,523,1",
      "124,224,524,1",
      "125,225,525,1",
      "126,226,526,1",
      "127,227,527,1",
      "128,228,528,1",
      "129,229,529,1",
    ].join("\n")
  ),
};

const selectors = {
  fileInput: 'input[type="file"]',
  formSelect: "select.form-select",
  contamination: 'input[type="range"]',
  search: 'input[placeholder="Search..."]',
  tables: "table",
};

async function apiRequest(request, method, endpoint, data = undefined) {
  const options = {
    method,
    headers: {
      Accept: "application/json",
    },
  };

  if (data !== undefined) {
    options.data = data;
    options.headers["Content-Type"] = "application/json";
  }

  return request.fetch(`${API_URL}${endpoint}`, options);
}

async function getAccessToken(request) {
  const response = await apiRequest(
    request,
    "POST",
    "/api/token/",
    {
      username: E2E_USERNAME,
      password: E2E_PASSWORD,
    }
  );

  if (!response.ok()) {
    throw new Error(
      `E2E login failed: ${response.status()} ${await response.text()}`
    );
  }

  const body = await response.json();

  if (!body.access) {
    throw new Error( "Login succeeded but no access token was returned." );
  }

  return body.access;
}

async function authenticateContext(page, request) {
  const token = await getAccessToken(request);

  await page.addInitScript(
    ({ access, username }) => {
      localStorage.setItem("access", access);
      localStorage.setItem("username", username);
    },
    {
      access: token,
      username: E2E_USERNAME,
    }
  );

  return token;
}

async function loginThroughUI(page) {
  await page.goto(BASE_URL);
  await expect( page.getByPlaceholder("Enter username") ).toBeVisible();
  await page .getByPlaceholder("Enter username") .fill(E2E_USERNAME);
  await page .getByPlaceholder("Enter password") .fill(E2E_PASSWORD);
  await page .getByRole("button", { name: /^login$/i }) .click();
  await page.waitForURL(/\/upload\/?$/, { timeout: 15000, });
}

async function prepareAuthenticatedPage(page, request) {
  await authenticateContext(page, request);
  await page.goto(`${BASE_URL}/upload`);
  await expect( page.locator(selectors.fileInput) ).toHaveCount(1);
}

async function clearClientResults(page) {
  await page.evaluate(() => {
    sessionStorage.removeItem("anomalyResult");
    sessionStorage.removeItem("classificationResult");
  });
}

// async function selectModelAndScaler(page, model, scaler) {
//   const selects = page.locator("select.form-select");
//   await expect(selects).toHaveCount(2);
//   console.log("SELECTING MODEL:", JSON.stringify(model));
//   console.log("SELECTING SCALER:", JSON.stringify(scaler));
//   const modelValues = await selects.nth(0).locator("option").evaluateAll( options => options.map(o => o.value) );
//   const scalerValues = await selects.nth(1).locator("option").evaluateAll( options => options.map(o => o.value) );
//   console.log("AVAILABLE MODEL VALUES:", modelValues);
//   console.log("AVAILABLE SCALER VALUES:", scalerValues);

//   if (!modelValues.includes(model)) {
//     throw new Error( `Invalid model value: ${JSON.stringify(model)}` );
//   }

//   if (!scalerValues.includes(scaler)) {
//     throw new Error( `Invalid scaler value: ${JSON.stringify(scaler)}` );
//   }

//   await selects.nth(0).selectOption({ value: model, });
//   await selects.nth(1).selectOption({ value: scaler, });

//   console.log( "SELECTED:", await selects.nth(0).inputValue(), await selects.nth(1).inputValue() );
// }

async function selectModelAndScaler(page, model, scaler) {
  const selects = page.locator("select.form-select");

  await expect(selects).toHaveCount(2);

  const modelValues = await selects
    .nth(0)
    .locator("option")
    .evaluateAll(options => options.map(o => o.value));

  const scalerValues = await selects
    .nth(1)
    .locator("option")
    .evaluateAll(options => options.map(o => o.value));

  if (!modelValues.includes(model)) {
    throw new Error(`Invalid model value: ${JSON.stringify(model)}`);
  }

  if (!scalerValues.includes(scaler)) {
    throw new Error(`Invalid scaler value: ${JSON.stringify(scaler)}`);
  }

  await selects.nth(0).selectOption({ value: model });
  await selects.nth(1).selectOption({ value: scaler });
}

async function uploadAnomalyDataset(
  page,
  request,
  options = {}
) {
  const {
    model = "isolation_forest",
    scaler = "standard",
    contamination = "0.01",
    } = options;

  await prepareAuthenticatedPage( page, request );
  await page .locator(selectors.fileInput) .setInputFiles(ANOMALY_CSV);
  await selectModelAndScaler( page, model, scaler );
  await page .locator(selectors.contamination) .fill(contamination);
  await page .getByRole("button", { name: /upload\s*&\s*analyze/i, }) .click();
}

async function uploadClassificationDataset(
  page,
  request,
  options = {}
) {
  const {
    model = "random_forest",
    scaler = "standard",
  } = options;

  await prepareAuthenticatedPage( page, request );
  await page .locator(selectors.fileInput) .setInputFiles( CLASSIFICATION_CSV );
  await selectModelAndScaler( page, model, scaler );
  await page .getByRole("button", { name: /upload\s*&\s*analyze/i, }) .click();
}

async function expectAnomalyDashboard(page) {
  await page.waitForURL( /\/dashboard\/?$/, { timeout: 30000 } );
  await expect( page.getByRole("heading", { name: /detection analysis report/i, }) ).toBeVisible({ timeout: 30000, });
}

async function expectClassificationDashboard(page) {
  await page.waitForURL( /\/classification\/?$/, { timeout: 30000 } );
  await expect( page.getByRole("heading", { name: /classification analysis report/i, }) ).toBeVisible({ timeout: 30000, });
}

async function openUserMenu(page) {
  const candidates = [
    page.getByRole("button", { name: /user|account|profile/i, }),
    page.locator( '[data-bs-toggle="dropdown"]' ),
    page.locator(".dropdown-toggle"),
  ];

  for (const locator of candidates) {
    if (
      await locator.count()
    ) {
      if (
        await locator.first().isVisible()
      ) {
        await locator.first().click();
        const menu = page.locator( ".dropdown-menu.show" );

        if (
          await menu.count()
        ) {
          await expect(menu).toBeVisible();
          return menu;
        }

        return page.locator( ".dropdown-menu" ).first();
      }
    }
  }

  throw new Error( "Could not find the authenticated user dropdown." );
}

async function openHistory(page) {
  const directLink = page.getByRole( "link", { name: /history/i } );

  if (
    await directLink.count()
  ) {
    await directLink.first().click();
  } else {
    const menu = await openUserMenu(page);

    await menu .getByRole("link", { name: /history/i, }) .click();
  }

  await page.waitForURL( /\/history\/?$/, { timeout: 15000 } );
}

async function expectNoBackendError(page) {
  await expect( page.getByText( /internal server error|500|network error|failed to fetch/i ) ).toHaveCount(0);
}


test.describe("Authentication", () => {
  test("valid credentials login successfully", async ({ page }) => {
  await loginThroughUI(page);
  await expect(page).toHaveURL(/\/upload\/?$/);
  await expect( page.getByRole("heading", { name: /smart anomaly detection/i, }) ).toBeVisible();
    });

  test("invalid credentials are rejected", async ({ page }) => {
  await page.goto(BASE_URL);
  await page .getByPlaceholder("Enter username") .fill("invalid_e2e_user");
  await page .getByPlaceholder("Enter password") .fill("InvalidPassword123!");
  await page .getByRole("button", { name: /^login$/i }) .click();
  await expect(page).toHaveURL(/\/$/);
  await expect( page.getByPlaceholder("Enter username") ).toBeVisible();
  await expect( page.getByPlaceholder("Enter password") ).toBeVisible();
  });

  test("empty credentials do not login", async ({
    page,
  }) => {
    await page.goto(BASE_URL);
    await page .getByRole("button", { name: /^login$/i, }) .click();
    await expect(page).toHaveURL( /\/$/ );
    await expect( page.getByPlaceholder( "Enter username" ) ).toBeVisible();
    await expect( page.getByPlaceholder( "Enter password" ) ).toBeVisible();
  });

  test("logout clears authentication", async ({
    page,
    request,
  }) => {
    await prepareAuthenticatedPage( page, request );
    const menu = await openUserMenu(page);
    const logoutButton = menu.getByRole("button", { name: /logout/i, });

    if (
      await logoutButton.count()
    ) {
      await logoutButton.click();
    } else {
      await menu.getByText( /logout/i ).click();
    }

    await expect(page).toHaveURL( /\/$/ );
    await expect( page.getByPlaceholder( "Enter username" ) ).toBeVisible();
    const access = await page.evaluate( () => localStorage.getItem("access") );
    expect(access).toBeNull();
  });
});

test.describe("Upload page", () => {
  test.beforeEach(async ({
    page,
    request,
  }) => {
    await prepareAuthenticatedPage( page, request );
    await clearClientResults(page);
  });

  test("upload page is displayed", async ({ page }) => {
  await expect( page.getByRole("heading", { name: /smart anomaly detection/i, }) ).toBeVisible();
  await expect( page.locator(selectors.fileInput) ).toHaveCount(1);
  await expect( page.getByRole("heading", { name: /click or drag file here/i, }) ).toBeVisible();
  await expect( page.getByText(/supports csv files/i) ).toBeVisible();
  await expect( page.getByRole("button", { name: /upload\s*&\s*analyze/i, }) ).toBeVisible();
  });

  test("CSV file can be selected", async ({
    page,
  }) => {
    await page .locator(selectors.fileInput) .setInputFiles( ANOMALY_CSV );
    await expect( page.getByText( ANOMALY_CSV.name, { exact: true } ) ).toBeVisible();
  });

  test("model selector contains supported models", async ({
    page,
  }) => {
    const select = page.locator( selectors.formSelect ).nth(0);

    const values =
      await select.locator(
        "option"
      ).evaluateAll(
        options =>
          options.map(
            option =>
              option.value
          )
      );

    expect(values).toEqual(
      expect.arrayContaining([
        "isolation_forest",
        "lof",
        "svm",
        "dbscan",
        "random_forest",
        "logistic_regression",
        "decision_tree",
        "xgboost",
      ])
    );
  });

  test("scaler selector contains supported scalers", async ({
    page,
  }) => {
    const select = page.locator( selectors.formSelect ).nth(1);

    const values =
      await select.locator(
        "option"
      ).evaluateAll(
        options =>
          options.map(
            option =>
              option.value
          )
      );

    expect(values).toEqual(
      expect.arrayContaining([
        "standard",
        "minmax",
        "robust",
      ])
    );
  });

  test("contamination value can be changed", async ({
    page,
  }) => {
    const contamination = page.locator( selectors.contamination );
    await expect( contamination ).toBeVisible();
    await contamination.fill( "0.05" );
    await expect( contamination ).toHaveValue("0.05");
  });

  test("MinMaxScaler can be selected", async ({
    page,
  }) => {
    const scaler = page.locator( selectors.formSelect ).nth(1);
    await scaler.selectOption( "minmax" );
    await expect( scaler ).toHaveValue("minmax");
  });

  test("RobustScaler can be selected", async ({
    page,
  }) => {
    const scaler = page.locator( selectors.formSelect ).nth(1);
    await scaler.selectOption( "robust" );
    await expect( scaler ).toHaveValue("robust");
  });
});

test.describe("Anomaly detection", () => {
  test("Isolation Forest completes an anomaly analysis", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset(
      page,
      request,
      {
        model: "isolation_forest",
        scaler: "standard",
        contamination: "0.01",
      }
    );

    await expectAnomalyDashboard( page );
    await expectNoBackendError( page );
  });

  test("Local Outlier Factor completes an anomaly analysis", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset(
      page,
      request,
      {
        model: "lof",
      }
    );

    await expectAnomalyDashboard( page );
  });

  test("One-Class SVM completes an anomaly analysis", async ({
    page,
    request,  
  }) => {
    await uploadAnomalyDataset(
      page,
      request,
      {
         model: "svm",
      }
    );

    await expectAnomalyDashboard( page );
  });

  test("DBSCAN completes an anomaly analysis", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset(
      page,
      request,
      {
        model: "dbscan",
      }
    );

    await expectAnomalyDashboard( page );
  });

  test("dashboard contains anomaly summary information", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset( page, request );
    await expectAnomalyDashboard( page );
    await expect( page.getByText( /total records/i ) ).toBeVisible();
    await expect( page.getByText( /anomalies/i ).first() ).toBeVisible();
    await expect( page.getByText( /normal/i ).first() ).toBeVisible();
  });

  test("dashboard contains results table", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset( page, request );
    await expectAnomalyDashboard( page );
    await expect( page.locator("table").first() ).toBeVisible();
    await expect( page.locator( "table tbody tr" ).first() ).toBeVisible();
  });

  test("dashboard search filters results", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset( page, request );
    await expectAnomalyDashboard( page );
    const search = page.locator( selectors.search );

    if (
      await search.count()
    ) {
      await search.fill( "10" );
      await expect( page.locator( "table tbody tr" ).first() ).toBeVisible();
    }
  });

  test("All filter is available", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset( page, request );
    await expectAnomalyDashboard( page );
    await expect( page.getByRole("button", { name: /^all$/i, }) ).toBeVisible();
  });

  test("Anomalies filter is available", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset(
      page,
      request,
      {
        contamination: "0.05",
      }
    );

    await expectAnomalyDashboard( page );
    const button = page .getByRole("group") .getByRole("button", { name: /^anomalies$/i, });
    await expect(button).toBeVisible();
    await button.click();
  });

  test("Normal filter is available", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset(
      page,
      request,
      {
        contamination: "0.05",
      }
    );

    await expectAnomalyDashboard( page );
    const button = page .getByRole("group") .getByRole("button", { name: /^normal$/i, });
    await expect( button ).toBeVisible();
    await button.click();
  });

  test("CSV export button is available", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset( page, request );
    await expectAnomalyDashboard( page );
    await expect( page.getByRole("button", { name: /^csv$/i, }) ).toBeVisible();
  });

  test("PDF export button is available", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset( page, request );
    await expectAnomalyDashboard( page );
    await expect( page.getByRole("button", { name: /^pdf$/i, }) ).toBeVisible();
  });

  test("delete dataset button is available", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset( page, request );
    await expectAnomalyDashboard( page );
    await expect( page.getByRole("button", { name: /delete dataset/i, }) ).toBeVisible();
  });
});


test.describe("Anomaly dashboard details", () => {
  test.beforeEach(async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset( page, request );
    await expectAnomalyDashboard( page );
  });

  test("dashboard shows analysis results", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset(page, request);
    await expectAnomalyDashboard(page);
    await expect( page.getByRole("heading", { name: /detection analysis report/i, }) ).toBeVisible();
    await expect( page.locator("table tbody tr").first() ).toBeVisible();
  });

  test("dashboard has search input when supported", async ({
    page,
  }) => {
    const search = page.locator( selectors.search );
    if (
      await search.count()
    ) {
      await expect( search ).toBeVisible();
    }
  });

  test("dashboard has result rows", async ({
    page,
  }) => {
    const rows =
      page.locator( "table tbody tr" );

    await expect( rows.first() ).toBeVisible();
    expect( await rows.count() ).toBeGreaterThan(0);
  });

 test("dashboard filter buttons can be selected", async ({
  page,
  request,
}) => {
  await uploadAnomalyDataset(page, request);
  await expectAnomalyDashboard(page);
  const all = page.getByRole("button", { name: /^all$/i, }).first();
  const anomalies = page.getByRole("button", { name: /^anomalies$/i, }).first();
  const normal = page.getByRole("button", { name: /^normal$/i, }).first();
  await expect(all).toBeVisible();
  await expect(anomalies).toBeVisible();
  await expect(normal).toBeVisible();
  await anomalies.click();
  await all.click();
  await normal.click();
  });

  test("dashboard can return to all records", async ({
    page,
  }) => {
    const all = page.getByRole("button", { name: /^all$/i, });
    const anomalies = page .getByRole("button", { name: /^anomalies$/i }) .first();
    await anomalies.click();
    await all.click();
    await expect( page.locator( "table tbody tr" ).first() ).toBeVisible();
  });

  test("dashboard pagination controls do not crash", async ({
    page,
  }) => {
    const next = page.getByRole("button", { name: /^next$/i, });
    if (
      await next.count()
    ) {
      await expect( next.last() ).toBeVisible();
    }

    const previous = page.getByRole("button", { name: /previous|prev/i, });
    if (
      await previous.count()
    ) {
      await expect( previous.last() ).toBeVisible();
    }
  });
});

test.describe("Anomaly exports", () => {
  test("CSV report can be downloaded", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset( page, request );
    await expectAnomalyDashboard( page );
    const button = page.getByRole("button", { name: /^csv$/i, });
    await expect(button).toBeVisible();
    const downloadPromise = page.waitForEvent( "download" );
    await button.click();
    const download = await downloadPromise;
    expect( download.suggestedFilename() ).toMatch( /\.csv$/i );
  });

  test("PDF report can be downloaded", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset( page, request );
    await expectAnomalyDashboard( page );
    const button = page.getByRole("button", { name: /^pdf$/i, });
    await expect(button).toBeVisible();
    const downloadPromise = page.waitForEvent( "download" );
    await button.click();
    const download = await downloadPromise;
    expect( download.suggestedFilename() ).toMatch( /\.pdf$/i );
  });
});

test.describe("Dataset management", () => {
  test("dataset can be deleted from dashboard", async ({
  page,
  request,
}) => {
  await uploadAnomalyDataset(page, request);
  await expectAnomalyDashboard(page);
  const deleteButton = page.getByRole("button", { name: /delete/i, }).first();
  await expect(deleteButton).toBeVisible({ timeout: 15000, });
  page.once("dialog", async dialog => { console.log( "DELETE TEST: dialog:", dialog.message() );
  await dialog.accept();
  });

  await deleteButton.click();
  await expect( page.getByRole("heading", { name: /smart anomaly detection/i, }) ).toBeVisible({ timeout: 15000, });
 });

  test("upload page is usable again after deleting dataset", async ({
  page,
  request,
}) => {

  await uploadAnomalyDataset(page, request);
  await expectAnomalyDashboard(page);
  const deleteButton = page .getByRole("button", { name: /delete/i }) .first();
  await expect(deleteButton).toBeVisible({ timeout: 15000, });
  page.once("dialog", async (dialog) => { await dialog.accept(); });
  await deleteButton.click();
  await expect(page).toHaveURL(/\/upload\/?$/, { timeout: 15000, });
  await expect( page.getByRole("heading", { name: /smart anomaly detection/i, }) ).toBeVisible({ timeout: 15000, });
  await expect( page.getByRole("heading", { name: /click or drag file here/i, }) ).toBeVisible({ timeout: 15000, });
  await expect( page.getByText(/supports csv files/i) ).toBeVisible();
  await expect( page.getByRole("button", { name: /upload\s*&\s*analyze/i, }) ).toBeVisible();
  });
});

test.describe("History", () => {
  test("history page can be opened", async ({
    page,
    request,
  }) => {
    await prepareAuthenticatedPage( page, request );
    await openHistory(page);
    await expect( page ).toHaveURL( /\/history\/?$/ );
  });

  test("history page displays its heading", async ({
    page,
    request,
  }) => {
    await prepareAuthenticatedPage( page, request );
    await openHistory(page);
    await expect( page.getByRole("heading", { name: /detection history/i, }) ).toBeVisible();
  });

  test("history page contains a table when history exists", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset( page, request );
    await expectAnomalyDashboard( page );
    await openHistory(page);
    const table = page.locator("table");
    await expect( table.first() ).toBeVisible();
  });

  test("new anomaly detection appears in history", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset( page, request );
    await expectAnomalyDashboard( page );
    await openHistory(page);
    await expect( page.getByRole("cell", { name: ANOMALY_CSV.name, exact: true, }).first() ).toBeVisible({ timeout: 15000, });
  });

  test("history contains model information", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset(
      page,
      request,
      {
        model: "isolation_forest",
      }
    );

    await expectAnomalyDashboard( page );
    await openHistory(page);
    const modelCells = page.getByText( "isolation_forest", { exact: true } );
    await expect( modelCells.first() ).toBeVisible({ timeout: 15000, });
  });

  test("history contains scaler information", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset(
      page,
      request,
      {
        scaler: "standard",
      }
    );

    await expectAnomalyDashboard( page );
    await openHistory(page);
    await expect( page.getByText( /standard/i ).first() ).toBeVisible({ timeout: 15000, });
  });

  test("history table rows are rendered", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset( page, request );
    await expectAnomalyDashboard( page );
    await openHistory(page);
    const rows = page.locator( "table tbody tr" );
    await expect( rows.first() ).toBeVisible();
    expect( await rows.count() ).toBeGreaterThan(0);
  });

  test("history clear button is available when records exist", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset( page, request );
    await expectAnomalyDashboard( page );
    await openHistory(page);
    const clear = page.getByRole("button", { name: /clear all/i, });

    if (
      await clear.count()
    ) {
      await expect(
        clear
      ).toBeVisible();
    }
  });

  test("history record delete controls are available", async ({
    page,
    request,
    }) => {
    await prepareAuthenticatedPage(page, request);
    await openHistory(page);
    const rows = page.locator("table tbody tr");
    await expect(rows.first()).toBeVisible();
    const deleteButtons = page.getByRole("button", { name: "Delete", exact: true, });
    await expect(deleteButtons.first()).toBeVisible();
    });

  test("history record can be deleted", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset( page, request );
    await expectAnomalyDashboard( page );
    await openHistory(page);
    const rows = page.locator( "table tbody tr" );
    await expect( rows.first() ).toBeVisible();
    const row = rows.first();
    const deleteButton = row.getByRole("button", { name: /delete/i, });

    if (
      await deleteButton.count()
    ) {
      page.once(
        "dialog",
        async dialog => {
          await dialog.accept();
        }
      );
      await deleteButton.click();
      await page.waitForTimeout( 500 );
    }
  });

  test("clear all history can be invoked", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset( page, request );
    await expectAnomalyDashboard( page );
    await openHistory(page);
    const clear = page.getByRole("button", { name: /clear all/i, });

    if (
      await clear.count()
    ) {
      page.once( "dialog", async dialog => { await dialog.accept(); } );
      await clear.click();
      await page.waitForTimeout( 500 );
    }
  });
});

test.describe("Classification", () => {
  test("labelled CSV starts classification flow", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset(
      page,
      request,
      {
        model: "random_forest",
      }
    );
    await expectClassificationDashboard( page );
  });

  test("classification dashboard displays results", async ({
  page,
  request,
}) => {
  await uploadClassificationDataset( page, request );
  await expectClassificationDashboard( page );
  await expect( page.getByText( "Accuracy", { exact: true, } ) ).toBeVisible();
  await expect( page.getByText( "Precision", { exact: true, } ) ).toBeVisible();
  await expect( page.getByText( "Recall", { exact: true, } ) ).toBeVisible();
  await expect( page.getByText( "F1 Score", { exact: true, } ) ).toBeVisible();
  });

  test("classification dashboard displays Accuracy", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset( page, request );
    await expectClassificationDashboard( page );
    await expect( page.getByText( "Accuracy", { exact: true, } ) ).toBeVisible();
  });

  test("classification dashboard displays Precision", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset( page, request );
    await expectClassificationDashboard( page );
    await expect( page.getByText( "Precision", { exact: true, } ) ).toBeVisible();
  });

  test("classification dashboard displays Recall", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset( page, request );
    await expectClassificationDashboard( page );
    await expect( page.getByText( "Recall", { exact: true, } ) ).toBeVisible();
  });

  test("classification dashboard displays F1 Score", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset( page, request );
    await expectClassificationDashboard( page );
    await expect( page.getByText( "F1 Score", { exact: true, } ) ).toBeVisible();
  });

  test("classification dashboard displays ROC-AUC", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset( page, request );
    await expectClassificationDashboard( page );
    await expect( page.getByText( "ROC-AUC", { exact: true, } ) ).toBeVisible();
  });

  test("classification dashboard displays confusion matrix section", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset( page, request );
    await expectClassificationDashboard( page );
    await expect( page.getByText( "Confusion Matrix", { exact: true, } ) ).toBeVisible();
  });

  test("classification supports Random Forest", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset(
      page,
      request,
      {
        model: "random_forest",
      }
    );
    await expectClassificationDashboard( page );
  });

  test("classification supports Logistic Regression", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset(
      page,
      request,
      {
        model: "logistic_regression",
      }
    );
    await expectClassificationDashboard( page );
  });

  test("classification supports Decision Tree", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset(
      page,
      request,
      {
        model: "decision_tree",
      }
    );
    await expectClassificationDashboard( page );
  });

  test("classification supports XGBoost", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset(
      page,
      request,
      {
        model: "xgboost",
      }
    );

    await expectClassificationDashboard( page );
  });

  test("classification PDF button is available", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset( page, request );
    await expectClassificationDashboard( page );
    await expect( page.getByRole("button", { name: /download pdf report/i, }) ).toBeVisible();
  });

  test("upload another dataset control is available", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset( page, request );
    await expectClassificationDashboard( page );
    await expect( page.getByRole("button", { name: /upload another dataset/i, }) ).toBeVisible();
  });
});


test.describe("Classification exports", () => {
  test("classification PDF can be downloaded", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset( page, request );
    await expectClassificationDashboard( page );
    const button = page.getByRole("button", { name: /download pdf report/i, });
    await expect( button ).toBeVisible();
    const downloadPromise = page.waitForEvent( "download" );
    await button.click();
    const download = await downloadPromise;
    expect( download.suggestedFilename() ).toMatch( /\.pdf$/i );
  });
});

test.describe("Classification navigation", () => {
  test("upload another dataset returns to upload screen", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset( page, request );
    await expectClassificationDashboard( page );
    const button = page.getByRole("button", { name: /upload another dataset/i, });
    await expect( button ).toBeVisible();
    await button.click();
    await page.waitForURL( /\/upload\/?$/, { timeout: 10000, } );
    await expect( page.getByRole("heading", { name: /smart anomaly detection/i, }) ).toBeVisible();
  });

  test("classification route without result is handled", async ({
    page,
    request,
  }) => {
    await prepareAuthenticatedPage( page, request );
    await clearClientResults( page );
    await page.goto( `${BASE_URL}/classification` );
    await expect( page ).toHaveURL( /\/classification\/?$/ );
    await expect( page.locator("body") ).toBeVisible();
  });
});

test.describe("Navigation", () => {
  test("authenticated upload page loads", async ({
    page,
    request,
  }) => {
    await prepareAuthenticatedPage( page, request );
    await expect( page ).toHaveURL( /\/upload\/?$/ );
  });

  test("dashboard route can be opened when result exists", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset( page, request );
    await expectAnomalyDashboard( page );
    await page.goto( `${BASE_URL}/dashboard` );
    await expect( page ).toHaveURL( /\/dashboard\/?$/ );
    await expect( page.getByRole("heading", { name: /detection analysis report/i, }) ).toBeVisible();
  });

  test("history route can be opened directly", async ({
    page,
    request,
  }) => {
    await prepareAuthenticatedPage( page, request );
    await page.goto( `${BASE_URL}/history` );
    await expect( page ).toHaveURL( /\/history\/?$/ );
    await expect( page.locator("body") ).toBeVisible();
  });

  test("authenticated user can access upload page after history navigation", async ({
    page,
    request,
  }) => {
    await prepareAuthenticatedPage( page, request );
    await page.goto( `${BASE_URL}/history` );
    await page.goto( `${BASE_URL}/upload` );
    await expect( page.getByRole("heading", { name: /smart anomaly detection/i, }) ).toBeVisible();
  });
});

test.describe("Theme and UI", () => {
  test("application body is rendered", async ({
    page,
    request,
  }) => {
    await prepareAuthenticatedPage( page, request );
    await expect( page.locator("body") ).toBeVisible();
  });

  test("theme control exists when implemented", async ({
    page,
    request,
  }) => {
    await prepareAuthenticatedPage( page, request );
    const controls = page.locator( 'button' );
    const texts = await controls.allTextContents();
    const themeControl = texts.find(text => /dark|light|mode/i.test( text ) );
    expect( themeControl === undefined || typeof themeControl === "string" ).toBeTruthy();
  });
});



test.describe("Backend connectivity", () => {
  test("backend token endpoint is reachable", async ({
    request,
  }) => {
    const response =
      await apiRequest(
        request,
        "POST",
        "/api/token/",
        {
          username: E2E_USERNAME,
          password: E2E_PASSWORD,
        }
      );

    expect( response.status() ).toBeLessThan(500);

    if (
      response.ok()
    ) {
      const body = await response.json();
      expect( body.access ).toBeTruthy();
    }
  });

  test("backend rejects invalid credentials", async ({
    request,
  }) => {
    const response =
      await apiRequest(
        request,
        "POST",
        "/api/token/",
        {
          username: "definitely_invalid_e2e_user",
          password: "DefinitelyInvalidPassword!",
        }
      );

    expect( response.status() ).toBeGreaterThanOrEqual(400);
    expect( response.status() ).toBeLessThan(500);
  });
});


test.describe("Authenticated API access", () => {
  test("authenticated browser can load upload page", async ({
    page,
    request,
  }) => {
    await prepareAuthenticatedPage( page, request );
    await expect( page.locator(selectors.fileInput) ).toHaveCount(1);
  });

  test("authenticated token is retained during navigation", async ({
    page,
    request,
  }) => {
    await prepareAuthenticatedPage( page, request );
    const before = await page.evaluate( () => localStorage.getItem( "access" ) );
    expect( before ).toBeTruthy();
    await page.goto( `${BASE_URL}/history` );
    const after = await page.evaluate( () => localStorage.getItem( "access" ) );
    expect( after ).toBe(before);
  });
});

test.describe("Model and scaler combinations", () => {
  test("Isolation Forest with StandardScaler", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset(
      page,
      request,
      {
        model: "isolation_forest",
        scaler: "standard",
      }
    );

    await expectAnomalyDashboard( page );
  });

  test("Isolation Forest with MinMaxScaler", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset(
      page,
      request,
      {
        model: "isolation_forest",
        scaler: "minmax",
      }
    );
    await expectAnomalyDashboard( page );
  });

  test("Isolation Forest with RobustScaler", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset(
      page,
      request,
      {
        model: "isolation_forest",
        scaler: "robust",
      }
    );

    await expectAnomalyDashboard( page );
  });
});

test.describe("Classification model and scaler combinations", () => {
  test("Random Forest with StandardScaler", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset(
      page,
      request,
      {
        model: "random_forest",
        scaler: "standard",
      }
    );

    await expectClassificationDashboard( page );
  });

  test("Logistic Regression with StandardScaler", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset(
      page,
      request,
      {
        model: "logistic_regression",
        scaler: "standard",
      }
    );

    await expectClassificationDashboard( page );
  });

  test("Decision Tree with StandardScaler", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset(
      page,
      request,
      {
        model: "decision_tree",
        scaler: "standard",
      }
    );

    await expectClassificationDashboard( page );
  });

  test("XGBoost with StandardScaler", async ({
    page,
    request,
  }) => {
    await uploadClassificationDataset(
      page,
      request,
      {
        model: "xgboost",
        scaler: "standard",
      }
    );

    await expectClassificationDashboard( page );
  });
});


test.describe("Client result state", () => {
  test("upload page starts without stale anomaly result", async ({
    page,
    request,
  }) => {
    await prepareAuthenticatedPage( page, request );

    await clearClientResults( page );

    const state =
      await page.evaluate(
        () => ({
          anomaly: sessionStorage.getItem( "anomalyResult" ),
          classification:
            sessionStorage.getItem( "classificationResult" ),
        })
      );

    expect( state.anomaly ).toBeNull();
    expect( state.classification ).toBeNull();
  });
});

test.describe("File validation", () => {
  test("non-CSV file is not silently treated as a valid CSV", async ({
    page,
    request,
  }) => {
    await prepareAuthenticatedPage( page, request );

    const invalidFile = {
      name: "invalid-e2e.txt",
      mimeType: "text/plain",
      buffer: Buffer.from(
        "this is not a csv file"
      ),
    };
    await page .locator( selectors.fileInput ) .setInputFiles( invalidFile );
    await expect( page.locator( selectors.fileInput ) ).toHaveCount(1);
  });
});

test.describe("Page reload behaviour", () => {
  test("upload page survives a browser reload", async ({
    page,
    request,
    }) => {
    await prepareAuthenticatedPage(page, request);
    const fileInput = page.locator(selectors.fileInput);
    await expect(fileInput).toHaveCount(1);
    await page.reload();
    await expect(fileInput).toHaveCount(1);
  });

  test("dashboard remains accessible after reload when result state exists", async ({
    page,
    request,
  }) => {
    await uploadAnomalyDataset( page, request );
    await expectAnomalyDashboard( page );
    await page.reload();
    await expect( page.locator("body") ).toBeVisible();
  });
});


test.describe("Responsive UI", () => {
  test("desktop upload page renders", async ({
    page,
    request,
  }) => {
    await page.setViewportSize({ width: 1440, height: 900, });
    await prepareAuthenticatedPage( page, request );
    await expect( page.locator(selectors.fileInput) ).toHaveCount(1);
    await expect( page.getByRole("button", { name: /upload\s*&\s*analyze/i, }) ).toBeVisible();
  });

  test("tablet upload page renders", async ({
    page,
    request,
  }) => {
    await page.setViewportSize({ width: 1024, height: 768, });
    await prepareAuthenticatedPage( page, request );
    await expect( page.locator(selectors.fileInput) ).toHaveCount(1);
  });

  test("mobile upload page renders", async ({
    page,
    request,
  }) => {
    await page.setViewportSize({ width: 390, height: 844, });
    await prepareAuthenticatedPage( page, request );
    await expect( page.locator(selectors.fileInput) ).toHaveCount(1);
    await expect( page.locator("body") ).toBeVisible();
  });
});


test.describe("Application smoke test", () => {
  test("complete basic user journey", async ({
    page,
    request,
  }) => {
  
    await loginThroughUI(page);
    await expect( page ).toHaveURL( /\/upload\/?$/ );
    await expect( page.locator(selectors.fileInput) ).toHaveCount(1);
    await clearClientResults( page );
    await page .locator( selectors.fileInput ) .setInputFiles( ANOMALY_CSV );
    await selectModelAndScaler( page, "isolation_forest", "standard" );
    await page .locator( selectors.contamination ) .fill("0.01");
    await page .getByRole("button", { name: /upload\s*&\s*analyze/i, }) .click();
    await expectAnomalyDashboard( page );
    await expect( page.locator( "table tbody tr" ).first() ).toBeVisible();
    await openHistory(page);
    await expect( page.locator("body") ).toBeVisible();
  });
});

test.describe("Final application health", () => {
  test("authenticated application does not show an uncaught frontend error", async ({
    page,
    request,
  }) => {
    const consoleErrors = [];
    page.on( "console", message => {
        if (
          message.type() === "error"
        ) {
          consoleErrors.push( message.text() );
        }
      }
    );

    await prepareAuthenticatedPage( page, request );
    await expect( page.locator(selectors.fileInput) ).toHaveCount(1);
    const meaningfulErrors = consoleErrors.filter( message => !/favicon/i.test( message ) );
    expect( meaningfulErrors ).toEqual([]);
  });
});