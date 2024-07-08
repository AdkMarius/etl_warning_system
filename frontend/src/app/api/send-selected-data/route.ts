import { NextRequest, NextResponse } from "next/server";
import {SelectedData} from "@/lib/datas-definition";
import {sendSelectedData} from "@/lib/datas";

export const dynamic = 'force-dynamic';

export async function POST(request: NextRequest) {
    const data: SelectedData = await request.json();

    const res = await sendSelectedData(data);

    const dataResponse = await res.json();

    return NextResponse.json(dataResponse);
}