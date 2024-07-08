import { NextRequest, NextResponse} from "next/server";
import {fetchFilteredIndicators} from "@/lib/datas";
import {DataResponse} from "@/lib/datas-definition";

export const dynamic = 'force-dynamic'

export async function POST(request: NextRequest) {
    const data = await request.json()

    const dataResponse: DataResponse = await fetchFilteredIndicators(data.page, data.query);

    return NextResponse.json(dataResponse);
}