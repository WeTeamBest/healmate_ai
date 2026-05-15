import { MainLayout, Card, Button } from '../components';

export default function GoalsPage() {
  return (
    <MainLayout title="Personal Goals">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <Card>
          <div className="text-center p-8">
            <p className="text-4xl mb-4">🎯</p>
            <h2 className="text-xl font-bold text-primary-dark mb-2">Set New Goal</h2>
            <p className="text-gray-600 mb-4">
              Tentukan tujuan untuk pemulihan dan pertumbuhan personal Anda
            </p>
            <Button variant="primary">Create Goal</Button>
          </div>
        </Card>

        <Card>
          <div className="text-center p-8">
            <p className="text-4xl mb-4">📋</p>
            <h2 className="text-xl font-bold text-primary-dark mb-2">My Goals</h2>
            <p className="text-gray-600 mb-4">
              Lihat progress dan manage semua goals yang sedang berjalan
            </p>
            <Button variant="secondary">View All</Button>
          </div>
        </Card>
      </div>

      <Card>
        <h2 className="text-xl font-bold text-primary-dark mb-4">📊 Goal Categories</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          <div className="p-4 bg-red-50 rounded-lg text-center">
            <p className="text-2xl mb-2">❤️</p>
            <p className="font-semibold">Emotional Healing</p>
            <p className="text-xs text-gray-600 mt-1">Pemulihan emosional</p>
          </div>
          <div className="p-4 bg-green-50 rounded-lg text-center">
            <p className="text-2xl mb-2">💪</p>
            <p className="font-semibold">Physical Wellness</p>
            <p className="text-xs text-gray-600 mt-1">Kesehatan fisik</p>
          </div>
          <div className="p-4 bg-blue-50 rounded-lg text-center">
            <p className="text-2xl mb-2">🧠</p>
            <p className="font-semibold">Mental Health</p>
            <p className="text-xs text-gray-600 mt-1">Kesehatan mental</p>
          </div>
          <div className="p-4 bg-purple-50 rounded-lg text-center">
            <p className="text-2xl mb-2">🌱</p>
            <p className="font-semibold">Personal Growth</p>
            <p className="text-xs text-gray-600 mt-1">Pertumbuhan personal</p>
          </div>
          <div className="p-4 bg-pink-50 rounded-lg text-center">
            <p className="text-2xl mb-2">👥</p>
            <p className="font-semibold">Relationships</p>
            <p className="text-xs text-gray-600 mt-1">Hubungan sosial</p>
          </div>
        </div>
      </Card>

      <Card className="mt-6">
        <h2 className="text-xl font-bold text-primary-dark mb-4">🎯 Active Goals</h2>
        <div className="text-center py-8 text-gray-400">
          <p>Belum ada goal yang aktif. Mulai dengan membuat goal pertama Anda!</p>
        </div>
      </Card>
    </MainLayout>
  );
}
