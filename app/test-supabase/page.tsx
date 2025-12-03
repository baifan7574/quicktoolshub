import { supabase } from '@/lib/supabase'

export default async function TestSupabase() {
  try {
    const { data, error } = await supabase
      .from('categories')
      .select('*')
      .limit(5)

    if (error) {
      return (
        <div className="p-8">
          <h1 className="text-2xl font-bold mb-4">Supabase连接测试</h1>
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            <p className="font-bold">连接错误：</p>
            <p>{error.message}</p>
            <p className="mt-2 text-sm">错误代码：{error.code}</p>
          </div>
        </div>
      )
    }

    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">✅ Supabase连接成功！</h1>
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          <p>成功连接到Supabase数据库</p>
        </div>
        <div className="mt-4">
          <h2 className="text-xl font-semibold mb-2">分类数据：</h2>
          <pre className="bg-gray-100 p-4 rounded overflow-auto">
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      </div>
    )
  } catch (error: any) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">Supabase连接测试</h1>
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          <p className="font-bold">错误：</p>
          <p>{error?.message || '未知错误'}</p>
        </div>
      </div>
    )
  }
}

