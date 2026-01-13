import { NextResponse } from 'next/server';
import OpenAI from 'openai';
import fs from 'fs';
import path from 'path';

// 读取本地 config.ini 获取 Key (因为 .env.local 之前有 gitignore 问题，临时方案)
// 在生产环境应使用 process.env
const getConfigKey = () => {
    try {
        // 1. 优先检查当前目录 (Production)
        let configPath = path.resolve(process.cwd(), 'config.ini');
        if (!fs.existsSync(configPath)) {
            // 2.而在开发环境，通常在上一级
            configPath = path.resolve(process.cwd(), '../config.ini');
        }

        if (fs.existsSync(configPath)) {
            const content = fs.readFileSync(configPath, 'utf-8');
            const match = content.match(/DEEPSEEK_API_KEY=(.*)/);
            if (match) return match[1].trim();
        }
    } catch (e) {
        console.error("Config read error", e);
    }
    return process.env.DEEPSEEK_API_KEY || '';
};

const apiKey = getConfigKey();

const client = new OpenAI({
    apiKey: apiKey,
    baseURL: 'https://api.deepseek.com', // DeepSeek V3 Endpoint
});

export async function POST(req: Request) {
    const { brand } = await req.json();

    if (!brand) {
        return NextResponse.json({ error: 'Brand is required' }, { status: 400 });
    }

    // 系统 Prompt：法律专家人设
    const systemPrompt = `You are a Senior International Trade Attorney specializing in IP litigation. 
    User is inquiring about the brand "${brand}".
    
    Task:
    1. Simulate a LIVE database check of US District Courts (N.D. Illinois, S.D. Florida).
    2. Generate a "preliminary risk assessment" (keep it tense and urgent).
    3. Output text must feel like a computer terminal log or a lawyer's dictation.
    4. Mention "Potential TRO (Temporary Restraining Order)" and "Asset Freeze Risk".
    
    Format:
    - Start with timestamp logs.
    - Use uppercase for critical alerts.
    - Keep it under 150 words for the preview.`;

    try {
        // 真实调用 DeepSeek (注释掉以节省 Token，Demo 阶段可开启)
        const completion = await client.chat.completions.create({
            model: "deepseek-chat",
            messages: [
                { role: "system", content: systemPrompt },
                { role: "user", content: `Analyze risk for: ${brand}` },
            ],
            stream: true,
        });

        // 创建流式响应 (Streaming Response)
        const encoder = new TextEncoder();
        const customStream = new ReadableStream({
            async start(controller) {
                for await (const chunk of completion) {
                    const content = chunk.choices[0]?.delta?.content || '';
                    if (content) {
                        controller.enqueue(encoder.encode(content));
                    }
                }
                controller.close();
            },
        });

        return new NextResponse(customStream, {
            headers: {
                'Content-Type': 'text/plain; charset=utf-8',
                'Transfer-Encoding': 'chunked',
            },
        });

    } catch (error) {
        console.error("AI Error:", error);
        return NextResponse.json({ error: 'DeepSeek API connection failed.' }, { status: 500 });
    }
}
