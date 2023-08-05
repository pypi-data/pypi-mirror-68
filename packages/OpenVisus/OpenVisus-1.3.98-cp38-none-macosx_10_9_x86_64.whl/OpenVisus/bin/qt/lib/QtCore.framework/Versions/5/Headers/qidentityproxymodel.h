/****************************************************************************
**
** Copyright (C) 2011 Klarälvdalens Datakonsult AB, a KDAB Group company, info@kdab.com, author Stephen Kelly <stephen.kelly@kdab.com>
** Contact: https://www.qt.io/licensing/
**
** This file is part of the QtGui module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:LGPL$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** GNU Lesser General Public License Usage
** Alternatively, this file may be used under the terms of the GNU Lesser
** General Public License version 3 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPL3 included in the
** packaging of this file. Please review the following information to
** ensure the GNU Lesser General Public License version 3 requirements
** will be met: https://www.gnu.org/licenses/lgpl-3.0.html.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 2.0 or (at your option) the GNU General
** Public license version 3 or any later version approved by the KDE Free
** Qt Foundation. The licenses are as published by the Free Software
** Foundation and appearing in the file LICENSE.GPL2 and LICENSE.GPL3
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-2.0.html and
** https://www.gnu.org/licenses/gpl-3.0.html.
**
** $QT_END_LICENSE$
**
****************************************************************************/


#ifndef QIDENTITYPROXYMODEL_H
#define QIDENTITYPROXYMODEL_H

#include <QtCore/qabstractproxymodel.h>

#ifndef QT_NO_IDENTITYPROXYMODEL

QT_BEGIN_NAMESPACE


class QIdentityProxyModelPrivate;

class Q_CORE_EXPORT QIdentityProxyModel : public QAbstractProxyModel
{
    Q_OBJECT
public:
    explicit QIdentityProxyModel(QObject* parent = Q_NULLPTR);
    ~QIdentityProxyModel();

    int columnCount(const QModelIndex& parent = QModelIndex()) const Q_DECL_OVERRIDE;
    QModelIndex index(int row, int column, const QModelIndex& parent = QModelIndex()) const Q_DECL_OVERRIDE;
    QModelIndex mapFromSource(const QModelIndex& sourceIndex) const Q_DECL_OVERRIDE;
    QModelIndex mapToSource(const QModelIndex& proxyIndex) const Q_DECL_OVERRIDE;
    QModelIndex parent(const QModelIndex& child) const Q_DECL_OVERRIDE;
    using QObject::parent;
    int rowCount(const QModelIndex& parent = QModelIndex()) const Q_DECL_OVERRIDE;
    QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const Q_DECL_OVERRIDE;
    bool dropMimeData(const QMimeData* data, Qt::DropAction action, int row, int column, const QModelIndex& parent) Q_DECL_OVERRIDE;
    QModelIndex sibling(int row, int column, const QModelIndex &idx) const Q_DECL_OVERRIDE;

    QItemSelection mapSelectionFromSource(const QItemSelection& selection) const Q_DECL_OVERRIDE;
    QItemSelection mapSelectionToSource(const QItemSelection& selection) const Q_DECL_OVERRIDE;
    QModelIndexList match(const QModelIndex& start, int role, const QVariant& value, int hits = 1, Qt::MatchFlags flags = Qt::MatchFlags(Qt::MatchStartsWith|Qt::MatchWrap)) const Q_DECL_OVERRIDE;
    void setSourceModel(QAbstractItemModel* sourceModel) Q_DECL_OVERRIDE;

    bool insertColumns(int column, int count, const QModelIndex& parent = QModelIndex()) Q_DECL_OVERRIDE;
    bool insertRows(int row, int count, const QModelIndex& parent = QModelIndex()) Q_DECL_OVERRIDE;
    bool removeColumns(int column, int count, const QModelIndex& parent = QModelIndex()) Q_DECL_OVERRIDE;
    bool removeRows(int row, int count, const QModelIndex& parent = QModelIndex()) Q_DECL_OVERRIDE;

protected:
    QIdentityProxyModel(QIdentityProxyModelPrivate &dd, QObject* parent);

private:
    Q_DECLARE_PRIVATE(QIdentityProxyModel)
    Q_DISABLE_COPY(QIdentityProxyModel)

    Q_PRIVATE_SLOT(d_func(), void _q_sourceRowsAboutToBeInserted(QModelIndex,int,int))
    Q_PRIVATE_SLOT(d_func(), void _q_sourceRowsInserted(QModelIndex,int,int))
    Q_PRIVATE_SLOT(d_func(), void _q_sourceRowsAboutToBeRemoved(QModelIndex,int,int))
    Q_PRIVATE_SLOT(d_func(), void _q_sourceRowsRemoved(QModelIndex,int,int))
    Q_PRIVATE_SLOT(d_func(), void _q_sourceRowsAboutToBeMoved(QModelIndex,int,int,QModelIndex,int))
    Q_PRIVATE_SLOT(d_func(), void _q_sourceRowsMoved(QModelIndex,int,int,QModelIndex,int))

    Q_PRIVATE_SLOT(d_func(), void _q_sourceColumnsAboutToBeInserted(QModelIndex,int,int))
    Q_PRIVATE_SLOT(d_func(), void _q_sourceColumnsInserted(QModelIndex,int,int))
    Q_PRIVATE_SLOT(d_func(), void _q_sourceColumnsAboutToBeRemoved(QModelIndex,int,int))
    Q_PRIVATE_SLOT(d_func(), void _q_sourceColumnsRemoved(QModelIndex,int,int))
    Q_PRIVATE_SLOT(d_func(), void _q_sourceColumnsAboutToBeMoved(QModelIndex,int,int,QModelIndex,int))
    Q_PRIVATE_SLOT(d_func(), void _q_sourceColumnsMoved(QModelIndex,int,int,QModelIndex,int))

    Q_PRIVATE_SLOT(d_func(), void _q_sourceDataChanged(QModelIndex,QModelIndex,QVector<int>))
    Q_PRIVATE_SLOT(d_func(), void _q_sourceHeaderDataChanged(Qt::Orientation orientation, int first, int last))

    Q_PRIVATE_SLOT(d_func(), void _q_sourceLayoutAboutToBeChanged(const QList<QPersistentModelIndex> &sourceParents, QAbstractItemModel::LayoutChangeHint hint))
    Q_PRIVATE_SLOT(d_func(), void _q_sourceLayoutChanged(const QList<QPersistentModelIndex> &sourceParents, QAbstractItemModel::LayoutChangeHint hint))
    Q_PRIVATE_SLOT(d_func(), void _q_sourceModelAboutToBeReset())
    Q_PRIVATE_SLOT(d_func(), void _q_sourceModelReset())
};

QT_END_NAMESPACE

#endif // QT_NO_IDENTITYPROXYMODEL

#endif // QIDENTITYPROXYMODEL_H

