import {SelectedData} from "@/lib/datas-definition";
import axios from "axios";

const api_url = process.env.API_URL;

export async function fetchFilteredDataElements(page: string | number, query?: string) {
    try {
        if (query) {
            const res = await fetch(
                api_url + `/dataElements?filter=${query}`,
                { cache: 'no-store'}
            );
            return res.json();
        } else {
            const res = await fetch(
                api_url + `/dataElements?page=${page}`,
                { cache: 'no-store'}
            );
            return res.json();
        }
    } catch (error) {
        console.error("API Error", error);
        throw new Error("Failed to fetch data elements.");
    }
}

export async function fetchFilteredDiseases(page: string | number, query?: string, filterType?: string) {
    try {
        if (query && filterType) {
            const res = await fetch(
                api_url + `/diseases?filter=${query}&filterType=${filterType}`,
                { cache: 'no-store'});
            return res.json();
        } else {
            const res = await fetch(
                api_url + `/diseases?page=${page}`,
                { cache: 'no-store'});
            return res.json();
        }
    } catch (error) {
        console.error("API Error", error);
        throw new Error("Failed to fetch diseases list.");
    }
}

export async function fetchFilteredIndicators(page: string | number, query?: string) {
    try {
        if (query) {
            const res = await fetch(api_url + `/indicators?filter=${query}`, { cache: 'no-store'});
            return res.json();
        } else {
            const res = await fetch(api_url + `/indicators?${page}`, { cache: 'no-store'});
            return res.json();
        }
    } catch (error) {
        console.error("API Error", error);
        throw new Error("Failed to fetch indicators data.");
    }
}

export async function sendSelectedData(data: SelectedData) {
    try {
        return await fetch(api_url + '/create-new-indicator', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
    } catch (error) {
        console.error("API Error: ", error);
        throw new Error("Failed to create new indicator for disease.");
    }
}