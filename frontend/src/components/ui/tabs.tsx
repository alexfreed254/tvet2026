import * as React from 'react';

interface TabsProps { defaultValue?: string; children: React.ReactNode; }
export function Tabs({ defaultValue, children }: TabsProps) {
  const [active, setActive] = React.useState(defaultValue || '');
  return <div className="tabs-container" data-active={active}>{children}</div>;
}

interface TabsListProps { children: React.ReactNode; }
export function TabsList({ children }: TabsListProps) {
  return <div className="flex space-x-1 rounded-lg bg-muted p-1">{children}</div>;
}

interface TabsTriggerProps { value: string; children: React.ReactNode; }
export function TabsTrigger({ value, children }: TabsTriggerProps) {
  const container = (document.querySelector('.tabs-container') as any);
  const active = container?.dataset?.active;
  return <button onClick={() => { if (container) container.dataset.active = value; }} className={`inline-flex items-center justify-center whitespace-nowrap rounded-md px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none ${active === value ? 'bg-background text-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'}`}>{children}</button>;
}

interface TabsContentProps { value: string; children: React.ReactNode; }
export function TabsContent({ value, children }: TabsContentProps) {
  const container = (document.querySelector('.tabs-container') as any);
  const active = container?.dataset?.active;
  if (active !== value) return null;
  return <div className="mt-2 ring-offset-background focus-visible:outline-none">{children}</div>;
}
