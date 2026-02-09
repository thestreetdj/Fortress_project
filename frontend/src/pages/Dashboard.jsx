import React, { useEffect, useState } from 'react';
import api from '../api/axios';

export default function Dashboard() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    api.get('/products/').then(res => setProducts(res.data));
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">재고 및 자산 현황</h1>
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-4">품목명</th>
              <th className="p-4 text-right">현재고</th>
              <th className="p-4">상태</th>
            </tr>
          </thead>
          <tbody>
            {products.map(p => (
              <tr key={p.id} className="border-t">
                <td className="p-4">{p.name}</td>
                <td className="p-4 text-right font-mono">{p.current_stock.toLocaleString()}</td>
                <td className="p-4">
                  <span className={`px-2 py-1 rounded text-xs ${p.current_stock < 10 ? 'bg-red-100 text-red-600' : 'bg-green-100 text-green-600'}`}>
                    {p.current_stock < 10 ? '재고부족' : '안전'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}