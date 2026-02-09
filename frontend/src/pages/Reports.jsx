import React, { useEffect, useState } from 'react';
import api from '../api/axios';

export default function Reports() {
  const [unpaidData, setUnpaidData] = useState([]);

  useEffect(() => {
    api.get('/reports/receivables-payables').then(res => setUnpaidData(res.data));
  }, []);

  return (
    <div className="p-8 space-y-8">
      <h1 className="text-2xl font-bold">통계 및 현황</h1>
      
      {/* 미수금/미지급 현황 리스트 */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h2 className="text-lg font-semibold mb-4 text-blue-600">거래처별 잔액 현황</h2>
        <div className="space-y-3">
          {unpaidData.map((item, idx) => (
            <div key={idx} className="flex justify-between items-center p-3 bg-gray-50 rounded">
              <span className="font-medium text-gray-700">{item.name}</span>
              <span className={`font-bold ${item.amount > 0 ? 'text-green-600' : 'text-red-600'}`}>
                {item.amount > 0 ? `미수금: ${item.amount.toLocaleString()}원` : `미지급: ${Math.abs(item.amount).toLocaleString()}원`}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}