import { readAll } from "./read-all.js";

export const API_PATH = "/api";

export const ENDPOINTS = {
    group: `${API_PATH}/group`,
    user: `${API_PATH}/user`,
    message: `${API_PATH}/message`
};

export async function fetchJSON(url, param) {
    const response = await fetch(url, param);

    const responseString = String.fromCharCode(...(await readAll(response.body)));

    try {
        const obj = JSON.parse(responseString);

        return {
            response: response,
            obj: obj
        }
    } catch (_e) {
        return {
            response: response,
            body: responseString
        };
    }
}
