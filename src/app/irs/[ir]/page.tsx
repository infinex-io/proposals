import { notFound } from 'next/navigation';
import { Properties, Renderer } from '@/components/Document';
import { Header } from '@/components/Header';
import { Back, PageContainer, PageTitle } from '@/components/UI';
import { reader } from '@/lib/reader';
import { number } from '@/lib/util';
import keystatic from '@/../keystatic.config';

type Params = {
  ir: string;
};

const schema = keystatic.collections.irs.schema;
const fields = Object.keys(schema);

export async function generateStaticParams(): Promise<Params[]> {
  const topics = await reader.collections.irs.all();
  return topics.map((ir) => ({
    ir: ir.slug,
  }));
}

export default async function Page({ params }: { params: Params }) {
  const ir = await reader.collections.irs.read(params.ir, {
    resolveLinkedFiles: true,
  });

  if (!ir) return notFound();

  return (
    <PageContainer>
      <Header currentPage="XIPs" />
      <div className="my-8 flex border-t border-slate-800">
        <Back href="/irs">Back to all IRs</Back>
      </div>
      <div className="mb-4">
        <div className="inline-block rounded-md border border-slate-700 px-4 py-1 text-sm font-bold">
          IR-{number(ir.ir!)}
        </div>
      </div>
      <PageTitle>{ir.title}</PageTitle>
      <Properties fields={fields} data={ir} />
      <Renderer document={ir.content} />
    </PageContainer>
  );
}
