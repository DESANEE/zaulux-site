import { products } from '../../data/product-list';

export async function GET() {
  const searchData = products.map(p => ({
    slug: p.slug,
    title: p.title,
    category: p.category,
    description: p.description.slice(0, 200),
  }));
  return new Response(JSON.stringify(searchData), {
    headers: { 'Content-Type': 'application/json' },
  });
}
