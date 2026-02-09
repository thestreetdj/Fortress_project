import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function FinanceChart({ data }) {
  // data 예시: [{ month: '2026-01', income: 5000, expense: 3000 }, ...]
  return (
    <div className="h-80 w-full bg-white p-4 rounded-xl shadow-sm">
      <h3 className="text-lg font-bold mb-4">월별 수입/비용 현황</h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="income" fill="#3b82f6" name="수입" />
          <Bar dataKey="expense" fill="#ef4444" name="비용" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}