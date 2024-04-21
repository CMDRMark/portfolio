import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = 'http://127.0.0.1:8000';

export let options = {
    vus: 100,  // Number of virtual users
    duration: '1m',  // Duration of the test
};


export default function () {
    let payload = JSON.stringify({
        quantity: 10,
        symbol: 'EURUSD',
    });

    let params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    let response = http.post(`${BASE_URL}/orders`, payload, params);

    check(response, {
        'Order placed successfully': (r) => r.status === 201,
    });
}