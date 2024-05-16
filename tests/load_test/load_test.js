import http from "k6/http";
import { check, sleep } from "k6";

// Test configuration
export const options = {
    thresholds: {
        // Assert that 99% of requests finish within 3000ms.
        http_req_duration: ["p(99) < 3000"],
    },
    // Ramp the number of virtual users up and down
    // stages: [
    //     { duration: "10s", target: 50 },
    // ],
};

// Simulated user behavior
export default function () {
    let data = { username: 'vendedor', password: 'vendedor' }
    let res = http.post("http://127.0.0.1:8080/login", data);
    // Validate response status
    check(res, {
        "status was 200": (r) => r.status == 200,
        "cookie session included": (r) => r.cookies.session[0].value.length > 0
    });

    let sale_data = {
        'product_id[]': [1],
        'amount[]': [1],
        client_id: '99999'
    }
    let sale_res = http.post("http://127.0.0.1:8080/seller/process_sale", sale_data)

    check(sale_res, { "response was 200": (r) => r.status == 200,
                      "sale was successful": (r) => r.body.includes("Venta exitosa") })


    sleep(1);
}
